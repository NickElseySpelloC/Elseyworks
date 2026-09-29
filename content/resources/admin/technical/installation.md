---
date: '2026-05-03T13:34:04+10:00'
title: 'Installation and Configuration'
description: "How thie site was setup"
showTableOfContents: true
showBreadcrumbs: true
---

## Components
This site uses the following technologies

### Hugo

The main engine that generates the site content from the markdown files and Tailwind CSS

### Congo Theme

Implements the theme for the Elseyworks site 

### Cloudflare

Provides DNS services for elseyworks.com as well as automatic SSL (via Let's Encrypt) and the worker for Decap CMS authorisation.

### GitHub Pages

Hosts the actual site

### Decap CMS

The simple content management system. See the [CMS Guide](../cms-guide/index.md) for the end user manual.

## Installation

For the original installation of these components, see the following Notes in UpNote:

- [Hugo Implementation - Phase 1](upnote://x-callback-url/openNote?noteId=019dcc41-bb8a-71ef-9ee5-52840b169dee) for the setup of Hugo and the Congo theme.
- [Hugo Implementation - Phase 2](upnote://x-callback-url/openNote?noteId=019dcc41-af8d-738d-ada5-423d44958d02) for the Decap CMS + Github Pages + Cloudflare Implementation