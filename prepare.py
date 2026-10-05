"""Fetch pinned upstream WDA and apply the two USB-only changes."""
from hashlib import sha256
from pathlib import Path
import json
import difflib
import urllib.request
import zipfile

COMMIT = "db1ef4a05cdd984ca39e4d0d7484f08e83a32d42"
ARCHIVE_SHA256 = "1f55302090cd95d83e6696130d17c213a87328a6815e3c7205d395f15980c40e"
root = Path(__file__).resolve().parent
archive = root / "upstream.zip"
if not archive.exists():
    urllib.request.urlretrieve(f"https://codeload.github.com/appium/WebDriverAgent/zip/{COMMIT}", archive)
assert sha256(archive.read_bytes()).hexdigest() == ARCHIVE_SHA256, "Upstream archive hash mismatch"
source = root / "source"
assert not source.exists(), "Use a fresh build directory"
with zipfile.ZipFile(archive) as package:
    package.extractall(root)
(root / f"WebDriverAgent-{COMMIT}").rename(source)
target = source / "WebDriverAgentLib/Routing/FBWebServer.m"
text = target.read_text(encoding="utf-8")
original = text
changes = {
    "  [self initScreenshotsBroadcaster];": '  [FBLogger logFmt:@"USB-only build: MJPEG screenshots broadcaster disabled"];',
    "  NSString *bindingIP = FBConfiguration.bindingIPAddress;": '  NSString *bindingIP = @"127.0.0.1"; // USB-only build: never expose HTTP to network interfaces.',
}
for before, after in changes.items():
    assert text.count(before) == 1, f"Unexpected upstream source: {before}"
    text = text.replace(before, after)
target.write_text(text, encoding="utf-8", newline="\n")
(root / "patch.diff").write_text("".join(difflib.unified_diff(original.splitlines(True), text.splitlines(True), fromfile="upstream/FBWebServer.m", tofile="usb-only/FBWebServer.m")), encoding="utf-8")
metadata = {
    "upstream": "appium/WebDriverAgent", "tag": "v13.2.0", "commit": COMMIT,
    "sourceArchiveSHA256": ARCHIVE_SHA256,
    "patchedFile": "WebDriverAgentLib/Routing/FBWebServer.m",
    "patchedFileSHA256": sha256(target.read_bytes()).hexdigest(),
    "policy": {"httpInterface": "127.0.0.1", "mjpeg": "disabled", "onDemandScreenshot": "retained"},
}
(root / "build-info.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
print(json.dumps(metadata, indent=2))
