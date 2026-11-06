"""Tests for the scripts ai-factory installs in projects.

A small local web server plays the website (good pages, broken pages,
redirects) and the GitHub file server (for fetch-vendored). Run:
    python3 tests/test_scripts.py
Standard library only.
"""
import hashlib
import http.server
import json
import os
import pathlib
import subprocess
import sys
import tempfile
import threading
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
T = ROOT / "skills" / "ai-factory" / "templates"

GOOD = """<!doctype html><html lang="fr"><head><title>Le Mas</title>
<meta name="description" content="Restaurant en Provence">
<link rel="canonical" href="https://www.example.com/{path}">
<link rel="alternate" hreflang="en" href="https://www.example.com/en/{path}">
<script type="application/ld+json">{{"@type": "Restaurant", "name": "Le Mas"}}</script>
</head><body><h1>Le Mas</h1><a href="/">Accueil</a></body></html>"""

BAD = """<!doctype html><html><head><title></title>
<link rel="canonical" href="https://staging.example.com/bad">
<script type="application/ld+json">{not json}</script>
</head><body><h1>One</h1><h1>Two</h1></body></html>"""

FILES = {}  # path -> bytes, for the fake raw.githubusercontent.com


class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def send(self, code, body=b"", headers=None, ctype="text/html"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        for k, v in (headers or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        p = self.path
        if p.startswith("/raw/"):
            data = FILES.get(p[len("/raw"):])
            return self.send(200, data, ctype="text/plain") if data is not None else self.send(404)
        redirects = {
            "/old-good": (301, "/restaurants/le-mas"),
            "/old-wrong": (301, "/somewhere-else"),
            "/old-temp": (302, "/restaurants/le-mas"),
            "/old-chain": (301, "/hop"),
            "/hop": (301, "/restaurants/le-mas"),
            "/old-dead": (308, "/gone"),
            "/old-full": (301, "https://www.example.com/restaurants/le-mas"),
        }
        if p in redirects:
            code, loc = redirects[p]
            return self.send(code, headers={"Location": loc})
        if p in ("/restaurants/le-mas", "/en/restaurants/le-mas", "/", "/en/"):
            path = p.strip("/").removeprefix("en/")
            return self.send(200, GOOD.format(path=path).encode())
        if p == "/bad":
            return self.send(200, BAD.encode())
        if p == "/robots.txt":
            return self.send(200, b"User-agent: *\nDisallow: /", ctype="text/plain")
        if p == "/sitemap.xml":
            host = self.server.sitemap_host
            xml = f'<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://{host}/</loc></url></urlset>'
            return self.send(200, xml.encode(), ctype="application/xml")
        self.send(404)


class Server:
    def __enter__(self):
        self.httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.httpd.sitemap_host = "www.example.com"
        self.url = f"http://127.0.0.1:{self.httpd.server_address[1]}"
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()
        return self

    def __exit__(self, *a):
        self.httpd.shutdown()
        self.httpd.server_close()


def run(cmd, env=None, cwd=None):
    e = dict(os.environ)
    e.pop("GITHUB_STEP_SUMMARY", None)
    e.update(env or {})
    return subprocess.run(cmd, capture_output=True, text=True, env=e, cwd=cwd)


class Redirects(unittest.TestCase):
    def csv(self, rows):
        f = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False)
        f.write("old,new\n# comment\n" + "\n".join(rows) + "\n")
        f.close()
        return f.name

    def test_good_lines_pass(self):
        with Server() as s:
            r = run([sys.executable, T / "check-redirects.py", self.csv([
                "/old-good,/restaurants/le-mas",
                "https://old.example.com/old-full,https://www.example.com/restaurants/le-mas",
            ]), s.url])
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("2 of 2", r.stdout)

    def test_each_failure_is_caught_and_blocks(self):
        with Server() as s:
            r = run([sys.executable, T / "check-redirects.py", self.csv([
                "/old-wrong,/restaurants/le-mas",
                "/old-temp,/restaurants/le-mas",
                "/old-chain,/restaurants/le-mas",
                "/old-dead,/gone",
                "/missing,/restaurants/le-mas",
                "/no-new-column",
            ]), s.url])
        self.assertEqual(r.returncode, 1)
        self.assertIn("0 of 6", r.stdout)
        for text in ("redirects to /somewhere-else", "answers 302", "redirects to /hop", "the new page answers 404", "answers 404", "no new address"):
            self.assertIn(text, r.stdout)

    def test_warn_mode_never_fails(self):
        with Server() as s:
            r = run([sys.executable, T / "check-redirects.py", self.csv(["/old-wrong,/restaurants/le-mas"]), s.url],
                    env={"REDIRECTS_MODE": "warn"})
        self.assertEqual(r.returncode, 0)
        self.assertIn("::warning::", r.stdout)


class Seo(unittest.TestCase):
    def pages(self, *paths):
        f = tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False)
        f.write("# key pages\n" + "\n".join(paths) + "\n")
        f.close()
        return f.name

    def test_good_page_passes_and_writes_snapshot(self):
        snap = tempfile.mktemp(suffix=".json")
        with Server() as s:
            r = run([sys.executable, T / "seo-check.py", self.pages("/restaurants/le-mas"), s.url, "--snapshot", snap],
                    env={"PRODUCTION_URL": "https://www.example.com", "SEO_MODE": "block"})
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("0 problem(s)", r.stdout)
        data = json.load(open(snap))
        self.assertEqual(data["/restaurants/le-mas"]["jsonld"], ["Restaurant"])

    def test_bad_page_problems_are_listed(self):
        with Server() as s:
            r = run([sys.executable, T / "seo-check.py", self.pages("/bad", "/nowhere"), s.url],
                    env={"PRODUCTION_URL": "https://www.example.com", "SEO_MODE": "block"})
        self.assertEqual(r.returncode, 1)
        for text in ("declare its language", "no title", "no description", "2 main headings", "not to the production site", "not valid JSON", "answers 404"):
            self.assertIn(text, r.stdout)

    def test_sitemap_on_wrong_host_is_flagged(self):
        with Server() as s:
            s.httpd.sitemap_host = "staging.example.com"
            r = run([sys.executable, T / "seo-check.py", self.pages("/"), s.url],
                    env={"PRODUCTION_URL": "https://www.example.com"})
        self.assertEqual(r.returncode, 0)  # warn mode by default
        self.assertIn("not on the production site", r.stdout)
        self.assertIn("::warning::", r.stdout)

    def test_drift_reports_what_disappeared(self):
        prev = tempfile.mktemp(suffix=".json")
        json.dump({"/restaurants/le-mas": {"title": "Le Mas", "description": "Ancienne description", "canonical": "x", "h1": ["Le Mas"], "lang": "fr", "hreflang": ["en"], "jsonld": ["Restaurant"]},
                   "/old-page": {"title": "Old"}}, open(prev, "w"))
        with Server() as s:
            r = run([sys.executable, T / "seo-check.py", self.pages("/restaurants/le-mas"), s.url, "--previous", prev],
                    env={"PRODUCTION_URL": "https://www.example.com"})
        self.assertIn("description changed", r.stdout)
        self.assertIn("/old-page", r.stdout)


class Coverage(unittest.TestCase):
    def write(self, name, text):
        d = tempfile.mkdtemp()
        p = os.path.join(d, name)
        open(p, "w").write(text)
        return p

    def test_formats(self):
        cases = [
            ("coverage-summary.json", json.dumps({"total": {"lines": {"pct": 81.5}}}), "81.5"),
            ("coverage.json", json.dumps({"totals": {"percent_covered": 64.25}}), "64.25"),
            ("lcov.info", "SF:a\nLH:3\nLF:4\nend_of_record\nSF:b\nLH:1\nLF:4\nend_of_record\n", "50.0"),
            ("coverage.xml", '<?xml version="1.0"?><coverage line-rate="0.725"></coverage>', "72.5"),
            ("cover.txt", "a.go:1:\tf\t100.0%\ntotal:\t\t\t(statements)\t66.7%\n", "66.7"),
        ]
        for name, text, want in cases:
            out = tempfile.mktemp()
            r = run([sys.executable, T / "coverage-check.py", self.write(name, text), "--write", out])
            self.assertEqual(r.returncode, 0, name + r.stdout + r.stderr)
            self.assertEqual(open(out).read().strip(), want, name)

    def test_down_warns_then_blocks(self):
        rep = self.write("coverage-summary.json", json.dumps({"total": {"lines": {"pct": 70}}}))
        base = self.write("coverage.txt", "75\n")
        r = run([sys.executable, T / "coverage-check.py", rep, "--baseline", base])
        self.assertEqual(r.returncode, 0)
        self.assertIn("went down", r.stdout)
        r = run([sys.executable, T / "coverage-check.py", rep, "--baseline", base], env={"COVERAGE_MODE": "block"})
        self.assertEqual(r.returncode, 1)

    def test_same_or_up_passes_and_no_baseline_is_fine(self):
        rep = self.write("coverage-summary.json", json.dumps({"total": {"lines": {"pct": 75.1}}}))
        base = self.write("coverage.txt", "75.2\n")
        r = run([sys.executable, T / "coverage-check.py", rep, "--baseline", base], env={"COVERAGE_MODE": "block"})
        self.assertEqual(r.returncode, 0, r.stdout)  # within the 0.2 tolerance
        r = run([sys.executable, T / "coverage-check.py", rep, "--baseline", "/does/not/exist"], env={"COVERAGE_MODE": "block"})
        self.assertEqual(r.returncode, 0)
        self.assertIn("no reference", r.stdout)


class TestsAdded(unittest.TestCase):
    def repo(self, files):
        d = tempfile.mkdtemp()
        g = lambda *a: subprocess.run(["git", "-c", "user.email=t@t", "-c", "user.name=t", *a], cwd=d, check=True, capture_output=True)
        g("init", "-q", "-b", "main")
        g("commit", "-q", "--allow-empty", "-m", "base")
        base = subprocess.run(["git", "rev-parse", "HEAD"], cwd=d, capture_output=True, text=True).stdout.strip()
        for f in files:
            p = pathlib.Path(d, f)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text("x\n")
        g("add", "-A")
        g("commit", "-q", "-m", "change")
        return d, base

    def check(self, files, env=None):
        d, base = self.repo(files)
        return run(["bash", str(T / "tests-added.sh"), base, "HEAD"], env=env, cwd=d)

    def test_code_without_test_warns_then_blocks(self):
        r = self.check(["src/agenda.ts"])
        self.assertEqual(r.returncode, 0)
        self.assertIn("::warning::", r.stdout)
        r = self.check(["src/agenda.ts"], env={"TESTS_ADDED_MODE": "block"})
        self.assertEqual(r.returncode, 1)

    def test_code_with_test_passes(self):
        for test_file in ("src/agenda.test.ts", "tests/test_agenda.py", "pkg/agenda_test.go", "e2e/home.spec.ts"):
            r = self.check(["src/agenda.ts", test_file], env={"TESTS_ADDED_MODE": "block"})
            self.assertEqual(r.returncode, 0, test_file + r.stdout)

    def test_deleted_test_is_flagged_even_without_code(self):
        d, _ = self.repo(["src/agenda.test.ts", "src/agenda.ts"])
        g = lambda *a: subprocess.run(["git", "-c", "user.email=t@t", "-c", "user.name=t", *a], cwd=d, check=True, capture_output=True)
        before = subprocess.run(["git", "rev-parse", "HEAD"], cwd=d, capture_output=True, text=True).stdout.strip()
        g("rm", "-q", "src/agenda.test.ts")
        g("commit", "-q", "-m", "drop test")
        r = run(["bash", str(T / "tests-added.sh"), before, "HEAD"], cwd=d)
        self.assertEqual(r.returncode, 0)
        self.assertIn("deletes test files", r.stdout)
        self.assertIn("::warning::", r.stdout)
        r = run(["bash", str(T / "tests-added.sh"), before, "HEAD"], env={"TESTS_ADDED_MODE": "block"}, cwd=d)
        self.assertEqual(r.returncode, 1)

    def test_changes_on_main_meanwhile_are_not_counted(self):
        # The branch only touches docs; main meanwhile gained code and deleted a test.
        d, base = self.repo(["src/x.test.ts"])
        g = lambda *a: subprocess.run(["git", "-c", "user.email=t@t", "-c", "user.name=t", *a], cwd=d, check=True, capture_output=True, text=True)
        start = g("rev-parse", "HEAD").stdout.strip()
        g("switch", "-q", "-c", "feature")
        pathlib.Path(d, "README.md").write_text("docs\n")
        g("add", "-A"); g("commit", "-q", "-m", "docs")
        g("switch", "-q", "main")
        pathlib.Path(d, "src/other.ts").write_text("x\n")
        g("rm", "-q", "src/x.test.ts")
        g("add", "-A"); g("commit", "-q", "-m", "main moves on")
        r = run(["bash", str(T / "tests-added.sh"), "main", "feature"], env={"TESTS_ADDED_MODE": "block"}, cwd=d)
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("No code file changed", r.stdout)

    def test_docs_config_and_label_pass(self):
        self.assertEqual(self.check(["README.md", "docs/a.md", "astro.config.mjs"], env={"TESTS_ADDED_MODE": "block"}).returncode, 0)
        self.assertEqual(self.check(["src/a.ts"], env={"TESTS_ADDED_MODE": "block", "SKIP_TESTS_ADDED": "true"}).returncode, 0)


class FetchVendored(unittest.TestCase):
    def lock(self, files):
        d = tempfile.mkdtemp()
        entry = {"name": "demo", "repo": "acme/demo", "commit": "abc", "license": "MIT", "author": "Acme", "dest": ".claude/skills/demo", "files": files}
        p = os.path.join(d, "lock.json")
        json.dump({"entries": [entry]}, open(p, "w"))
        return p

    def test_good_files_install_with_source(self):
        FILES["/acme/demo/abc/skills/demo/SKILL.md"] = b"hello"
        FILES["/acme/demo/abc/skills/demo/ref/x.md"] = b"world"
        lock = self.lock([
            {"src": "skills/demo/SKILL.md", "dest": "SKILL.md", "sha256": hashlib.sha256(b"hello").hexdigest()},
            {"src": "skills/demo/ref/x.md", "dest": "ref/x.md", "sha256": hashlib.sha256(b"world").hexdigest()},
        ])
        proj = tempfile.mkdtemp()
        with Server() as s:
            r = run([sys.executable, T / "fetch-vendored.py", lock], env={"VENDOR_BASE_URL": s.url + "/raw"}, cwd=proj)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        dest = pathlib.Path(proj, ".claude/skills/demo")
        self.assertEqual((dest / "ref/x.md").read_text(), "world")
        self.assertIn("Licence: MIT", (dest / "SOURCE.md").read_text())

    def test_wrong_fingerprint_installs_nothing(self):
        FILES["/acme/demo/abc/SKILL.md"] = b"tampered"
        lock = self.lock([{"src": "SKILL.md", "dest": "SKILL.md", "sha256": hashlib.sha256(b"original").hexdigest()}])
        proj = tempfile.mkdtemp()
        with Server() as s:
            r = run([sys.executable, T / "fetch-vendored.py", lock], env={"VENDOR_BASE_URL": s.url + "/raw"}, cwd=proj)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("does not match", r.stderr + r.stdout)
        self.assertFalse(pathlib.Path(proj, ".claude").exists())

    def test_unsafe_paths_are_refused(self):
        FILES["/acme/demo/abc/a"] = b"x"
        lock = self.lock([{"src": "a", "dest": "../../escape", "sha256": hashlib.sha256(b"x").hexdigest()}])
        proj = tempfile.mkdtemp()
        with Server() as s:
            r = run([sys.executable, T / "fetch-vendored.py", lock], env={"VENDOR_BASE_URL": s.url + "/raw"}, cwd=proj)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("unsafe path", r.stderr + r.stdout)


class StartCheck(unittest.TestCase):
    def check(self, build, start, secs="2"):
        d = tempfile.mkdtemp()
        return run(["bash", str(T / "start-check.sh"), build, start, secs], env={"START_CHECK_LOG": os.path.join(d, "start.log")}, cwd=d)

    def test_missing_module_fails(self):
        r = self.check("true", "echo \"Error [ERR_MODULE_NOT_FOUND]: Cannot find module '/app/dist/x' imported from /app/dist/y.js\" >&2; exit 1")
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("cannot load a module", r.stdout)

    def test_missing_setting_passes(self):
        r = self.check("true", "echo 'Error: NEXT_PUBLIC_FIREBASE_PROJECT_ID is not set' >&2; exit 1")
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("loaded all its modules", r.stdout)

    def test_python_import_error_fails(self):
        r = self.check("true", "python3 -c 'import a_module_that_does_not_exist_xyz'")
        self.assertEqual(r.returncode, 1, r.stdout)

    def test_failed_build_fails(self):
        r = self.check("exit 3", "true")
        self.assertEqual(r.returncode, 1)
        self.assertIn("production build itself failed", r.stdout)

    def test_server_that_keeps_running_is_stopped_and_passes(self):
        r = self.check("true", "echo listening; sleep 30", secs="2")
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("listening", r.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=1)
