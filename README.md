# USB-only WebDriverAgent build

Builds an **unsigned** iPhone test runner from Appium WebDriverAgent v13.2.0,
pinned to commit `db1ef4a05cdd984ca39e4d0d7484f08e83a32d42` and a verified source ZIP SHA256.

Two changes in `FBWebServer.m`:

1. Force the HTTP interface to `127.0.0.1`, independent of environment overrides.
2. Do not start the MJPEG screenshot broadcaster. On-demand HTTP screenshots remain available.

Run the **Build USB-only WDA** workflow, download `wda-usb-only-unsigned`, verify
`SHA256SUMS`, then sign and install the IPA locally with your own Apple account.
No Apple credentials, provisioning profiles, pairing records, or device screenshots belong in this repository.
Unsigned artifacts are retained for 14 days. Re-run the workflow when needed.

Upstream source: https://github.com/appium/WebDriverAgent

The upstream BSD license is included in the build artifact. This is an independent
build, not an official Appium release. Device runtime and network checks are still
required; a successful build alone does not prove that an installed app is safe.
