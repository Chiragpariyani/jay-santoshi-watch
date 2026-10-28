# Jay Santoshi Watch: Website

The SEO-optimised website for **Jay Santoshi Watch**, a watch shop and watch & clock repair service at
Shop No. 1, Swapna Shilp Complex, Nigam Nagar, Chandkheda, Ahmedabad 382424.

It's a plain static site: fast HTML pages with no JavaScript framework, built by a small Python script.
The ready-to-deploy website is in the **`public/`** folder.

## What's inside (123 pages)

| Section | URL | Purpose |
| --- | --- | --- |
| Home | `/` | Main page for "watch shop / watch repair Chandkheda" |
| Services (10) | `/services/<service>/` | Watch repair, battery, strap, glass, servicing, clock repair, watches, wall clocks, accessories, gifts |
| Areas (44) | `/areas/<area>/` | One page per locality in Ahmedabad and Gandhinagar ("watch shop in Motera", etc.) |
| Area + service (44) | `/areas/<area>/<service>/` | Neighbouring areas × 4 key services ("watch battery replacement in Sabarmati") |
| Brands (10) | `/brands/<brand>/` | Titan, Sonata, Fastrack, Casio, Timex, Maxima, HMT, Fossil, Citizen, Ajanta & Orpat |
| Guides (8) | `/guides/<guide>/` | Answer-first articles for Google, AI Overviews, ChatGPT and Perplexity |
| FAQ, About, Contact | `/faq/`, `/about/`, `/contact/` | |

**SEO / AEO / GEO features**
- JSON-LD on every page: `Store`/`LocalBusiness` (name, address, phone and hours exactly as on Google), `Service`, `FAQPage`, `BreadcrumbList`, `Article`, `WebSite`
- A "Quick answer" box at the top of each page, so AI answer engines can quote it
- `sitemap.xml`, `robots.txt` (explicitly allows Google, Bing, ChatGPT, Claude, Perplexity and other bots), `llms.txt`
- Canonical URLs, Open Graph / Twitter cards, a social share image, geo meta tags
- Gujarati and Hindi search phrases on every service and area page
- Mobile-first design with a sticky Call / WhatsApp / Directions bar, and a Google Map embed

## Deploy (pick one)

**Vercel (recommended):** go to vercel.com → Add New → Project → import this repo → Deploy.
`vercel.json` already points to `public/`, so you don't need to change any settings.

**Netlify:** go to app.netlify.com → Add new site → Import from Git → pick this repo. `netlify.toml` is already set up.

**GitHub Pages:** go to Settings → Pages → Source: *GitHub Actions*, then in the Actions tab run "Deploy to GitHub Pages".

## After deploying: important steps

1. **Domain:** the site lives at https://www.jaysantoshi.watch (`SITE_URL` in `src/data.py`). The old `jay-santoshi-watch.vercel.app` address still works; every page's canonical tag points to the custom domain, so search engines index only www.jaysantoshi.watch.
2. **Google Search Console:** add the site, verify it, and submit `https://<your-domain>/sitemap.xml`.
3. **Bing Webmaster Tools:** import from Search Console. ChatGPT search uses Bing's index.
4. **Google Business Profile:** put the website URL in the "Website" field of your Maps listing.
5. **Keep NAP identical** (Name, Address, Phone) on Google, Justdial and every other listing.
6. Keep asking happy customers for Google reviews. Reviews are the biggest local ranking factor.

## Editing content

All the shop details, services, areas and brands are in **`src/data.py`**. The guide articles are in **`src/guides.py`**.
After editing, rebuild the site:

```bash
python3 src/build.py      # needs Python 3; Pillow is optional (for PNG icons)
```

Then commit and push. Vercel and Netlify redeploy automatically.

To add a new area, copy one entry in `AREAS`, change it, and rebuild. Its page, links and sitemap entry are created automatically.

## Home-page video

The hero video (`src/static/video/`) is made from the shop photos by `python3 src/make_video.py` (needs Pillow and ffmpeg).
The page shows the poster image instantly and only downloads the ~0.9 MB video after the page has loaded and the video is on screen.
It is skipped for data-saver, 2G and reduced-motion visitors, so page speed isn't affected.
To use a real video instead, replace `shop-tour.mp4` / `shop-tour.webm` (keep them short, muted and under ~1–2 MB) and `shop-tour-poster.webp`.
