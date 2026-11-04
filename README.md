# Maryland Eagles Eyes

The welcome page for **122eagles.com**, focused on Maryland, USA.

Static HTML and CSS with a public-domain photograph of the Chesapeake Bay Bridge. A tiny first-party
script starts the camera after the photograph decodes. No framework or
first-party tracking scripts. Signup loads Buttondown only after a reader opens
the on-site dialog. Visual direction
inspired by The Bridge's muted landscape, serif typography and open composition;
its code and branding are not reused. The photograph is by Carol M. Highsmith,
Library of Congress; see `public/assets/PHOTO-CREDIT.md`.

Preview with `python3 -m http.server 8012 --directory public`.

Vercel framework preset: Other. Production branch: `main`. Root directory:
repository root. Output directory: `public` (also set in `vercel.json`). No build
or install command is required. Website files live in `public/`; internal
continuation notes stay outside the published directory.

Push to `main` to deploy production automatically through the connected Vercel
project `122eagles` in `toluadetuyis-projects`.

Fonts: Lora and Instrument Sans, distributed under the SIL Open Font License;
see `public/assets/OFL-*.txt`. Font files are self-hosted.


Newsletter signup is connected to `https://buttondown.com/eagles` through its
supported embedded form. Readers stay on 122eagles.com; Buttondown handles
validation, confirmation and any verification inside the frame. No API key is
stored in the browser, and the public subscription endpoint is not called with
JavaScript fetch. The close button remains available throughout the flow.

Run `python3 tests/subscription-browser.py` against a local preview. Set
`EAGLES_TEST_URL` to test a deployment. Set `EAGLES_LIVE_FORM=1` to additionally
load the real Buttondown form and check email validation; this test does not
submit a subscription or send confirmation email. The other cases use a small
provider-frame fixture to exercise the website's modal behavior independently.
