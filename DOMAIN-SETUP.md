# Pointing a custom domain at the TrueMake site

The site is served by GitHub Pages from this repo (branch `master`, root).
Current address: https://tendaimusendo.github.io/truemake-site/

Replace `example.co.uk` below with the domain you bought.

## 1. DNS records at the registrar

Add these to the domain's DNS zone.

| Type  | Name | Value                     |
|-------|------|---------------------------|
| A     | @    | 185.199.108.153           |
| A     | @    | 185.199.109.153           |
| A     | @    | 185.199.110.153           |
| A     | @    | 185.199.111.153           |
| AAAA  | @    | 2606:50c0:8000::153       |
| AAAA  | @    | 2606:50c0:8001::153       |
| AAAA  | @    | 2606:50c0:8002::153       |
| AAAA  | @    | 2606:50c0:8003::153       |
| CNAME | www  | tendaimusendo.github.io   |

If the registrar offers a "proxy" or "CDN" toggle on records (Cloudflare does),
leave it off until the certificate has been issued.

## 2. Tell GitHub Pages about the domain

From this folder:

```
gh api -X PUT repos/TendaiMusendo/truemake-site/pages -f cname=example.co.uk
```

GitHub then writes a `CNAME` file into the repo and starts verifying DNS. Once
it verifies (minutes to an hour, depending on DNS propagation), enforce HTTPS:

```
gh api -X PUT repos/TendaiMusendo/truemake-site/pages -F https_enforced=true
```

## 3. Check

```
curl -sI https://example.co.uk | head -5
curl -sI https://www.example.co.uk | head -5
```

Both should return `HTTP/2 200`; the `www` address redirects to the apex.

## Optional: verify the domain at account level first

Prevents anyone else taking the domain over on GitHub Pages. Creates a TXT
record challenge to add at the registrar:

```
gh api -X POST user/pages/domains -f domain=example.co.uk
```
