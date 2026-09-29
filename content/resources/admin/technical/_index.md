---
date: '2026-05-03T13:34:04+10:00'
title: 'Technical Overview'
description: "A technical guide to the setup of this web site."
thumbnail: technical.png
showTableOfContents: true
showBreadcrumbs: true
---

## Installing the site on a new machine

```bash
cd ~/dev

git clone https://github.com/NickElseySpelloC/Elseyworks

git submodule update --init --recursive
```

## Documentation Available

- Using the Site (see below)
- [Front Matter Reference](front-matter.md)
- [Short Code Reference](short-code-reference.md)
- [Installation and Configuration](installation.md)

## Creating a new page

Use hugo to create a default page:

`hugo new content/resources/technical/index.md`

## Understanding index vs _index pages

- `/_index.md` — section (has children, renders as a list/branch)
- `index.md` — page (standalone leaf, no children allowed)

If a folder contains other content pages, it needs `/_index.md`

### Quick comparison

| Aspect | `_index.md` | `index.md` |
|:--|:--|:--|
| Bundle type | Branch | Leaf |
| Template | List/section | Single/page |
| Can have child pages | ✅ Yes | ❌ No |
| Can co-locate assets | ⚠️ Technically, but not ideal | ✅ Yes, that's the point |
| Congo layout param | e.g. `layout: list` | e.g. `layout: article` |

### _index.md — Branch Bundle

A folder containing `_index.md` is a **branch bundle**. It represents a _section_ or _list node_ in Hugo's content tree.

- It **can have child pages** nested beneath it
- Hugo renders it using a **list template** (e.g. `layouts/_default/list.html`)
- In Congo, this is where you set section-level front matter like `title`, `description`, and layout options that apply to the listing page for that section
- The content body in `_index.md` appears above the list of child pages (if the template supports it)
- To disable listing of the child pages, set the **layout** front matter field in the _index.md page to **simple**.
- Use a branch bundle folder when you want to have multiple pages in the same folder (like this folder)

**Example use:** `content/posts/_index.md` — the landing page for your blog section, which lists all posts beneath it.

### index.md — Leaf Bundle

A folder containing `index.md` (no underscore) is a **leaf bundle**. It represents a _single page_ that owns everything inside its folder.

- It **cannot have child pages** — Hugo treats everything inside the folder as assets belonging to _that one page_ (images, attachments, etc.)
- Hugo renders it using a **single/page template** (e.g. `layouts/_default/single.html`)
- In Congo, this gets the full single-page treatment — article layout, breadcrumbs, reading time, etc.

**Example use:** `content/posts/my-great-post/index.md` — a single blog post that co-locates its images in the same folder (`content/posts/my-great-post/hero.jpg`).

## Hugo Taxonomy and Content

When auto-generating the content for a branch bundle folder, tt's Hugo's taxonomy system doing the heavy lifting — the `_index.md file` itself doesn't contain any logic. Here's how the pieces connect:

1. Hugo scans all content for front matterWhen Hugo builds the site, it reads every page and collects their categories values. Any page with `categories: Nick` gets registered against the "Nick" taxonomy term.
2. Taxonomies are configured by defaultHugo has categories and tags as built-in taxonomies. You don't need to declare them — they just work. (You can see this in taxonomies.toml if you want to customise them.)
3. Hugo auto-generates term pagesFor every unique category value found, Hugo automatically generates a listing page at /categories//. For Nick that becomes `/categories/nick/`. These pages exist even without an `_index.md` file — Hugo generates them from the theme's term.html layout.
4. The (manually created) `_index.md` just provides metadataThe file you created at `content/categories/nick/_index.md` only supplies the title, description, and layout front matter. It overrides the defaults (e.g. giving it a nice title instead of just "Nick"). The actual list of matching posts is assembled by Hugo at build time and passed to the term.html template via .Data.Pages — the template doesn't care where those pages physically live.

## Page Front Matter Fields

These are the yaml format key / value pairs at the start of a markdown page. Front matter fields used across this site are documented in the [Front Matter](front-matter.md) page.

## Short Codes

Short codes are custom html insert blocks that can be used to create things like floating images, call out boxes, etc. Some of the more popular ones are documented below. See the [Short Code Reference](short-code-reference.md) for the full list.

## Images

### Image file locations

`/assets` — images that Hugo _processes_ through its image pipeline (resizing, cropping, format conversion, fingerprinting). You access these via Hugo's `resources.Get` function in templates. Congo uses this for things like the author photo.

`/static` — images that Hugo copies to the output _as-is_ with no processing. They're served directly at the same path, e.g. `static/images/uploads/my-photo.jpg` becomes [https://elseyworks.com/images/uploads/my-photo.jpg](https://elseyworks.com/images/uploads/my-photo.jpg).

### Cover and thumbnail images

Use the following front matter fields to control these aspects

- **thumbnail**: An image to be used on the list page thumbnail.
- **cover**: An image to be used as the article cover (hero) image.
- **feature**: An image to be used as the article cover (hero) image and also the thumbnail.

You can also just create a file with this name in the bundle folder (e.g. thumbnail.jpg), rather than specify the front matter field. See [feature cover and thumbnail images](https://jpanther.github.io/congo/docs/getting-started/#feature-cover-and-thumbnail-images)

The CMS will honor these settings as well. 

### Floating an Image

You can still float an image in a page. The page can live in the current folder or under /static:

> \{\{< img-float src="/img/home/cover-lynn_articles.jpg" side="left" width=800 >}}

### Captioned image (including floating captions)

Use this format to display an in-line a captioned image:

> \{\{< img-caption src="villa-spalletti-trivelli-2.jpg" caption="Villa Spalletti Trivelli" alt="" >}}

Use this format to float a captioned image

> \{\{< img-caption-float src="villa-spalletti-trivelli-2.jpg" side="left" caption="Villa Spalletti Trivelli" alt="" >}}

Both of these support width and height arguments also. 

### Clear a floating image

Use the clear-float shortcode to force any subsequent content to appear below the image:

> \{\{< clear-float >}}

## Content Controls

### Call outs

Creating an inline call out box in the document:

> \{\{< callout >}}<br>
> Your inline callout text here.<br>
> \{\{< /callout >}}

And a floating call out box:

> \{\{< callout-float side="left" width="70%" >}}<br>
> Your inline callout text here.<br>
> \{\{< /callout-float >}}

Use the clear-float shortcode to force any subsequent content to appear below the call out box:

> \{\{< clear-float >}}

### Story Lead

Format a pagagraph as a story lead (sub-title) - generally used at the start of a document:

> \{\{< lead >}}<br>
> Verona City Guide<br>
> \{\{< /lead >}}

## URL redirects

Use the aliases: front matter field in the relevant target page:

```
aliases:
  - /good-stuff/vfrflightplanner/
  - /old-path/flying-stuff/
```

## Hugo Server

Run the server locally and include draft pages:

```bash
hugo server -D
```

Clean up the cache / destination folder

```bash
hugo --cleanDestinationDir
```

## Deploying to Production

When you're ready to push to production, simply commit and push the changes to Github.

The github workflow (see `/.github/workflows/deploy.yml`) will (on the Github server):

- Check out the site 
- Setup Hugo 
- Build the site
- Deploy to Github pages: https://github.com/NickElseySpelloC/Elseyworks/deployments/github-pages

---
