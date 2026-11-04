# Maryland Eagles Eyes

The welcome page for **122eagles.com**, focused on Maryland, USA.

Static HTML and CSS with a public-domain photograph of the Chesapeake Bay Bridge. A tiny first-party
script starts the camera after the photograph decodes. No framework, tracking
or third-party runtime requests. Visual direction
inspired by The Bridge's muted landscape, serif typography and open composition;
its code and branding are not reused. The photograph is by Carol M. Highsmith,
Library of Congress; see `public/assets/PHOTO-CREDIT.md`.

Preview with `python3 -m http.server 8012 --directory public`.

Vercel framework preset: Other. Production branch: `main`. Root directory:
repository root. Output directory: `public` (also set in `vercel.json`). No build
or install command is required. Website files live in `public/`; internal
continuation notes stay outside the published directory.

Push to `main` to deploy production after the repository is connected to the
existing Vercel project `122eagles` in `toluadetuyis-projects`.

Fonts: Lora and Instrument Sans, distributed under the SIL Open Font License;
see `public/assets/OFL-*.txt`. Font files are self-hosted.
