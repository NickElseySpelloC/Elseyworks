---
title: "CMS Guide"
description: "Guide to posting a blog or article on ElseyWorld using Content Management Systems (CMS)"
date: '2026-04-14T17:00:39+10:00'
thumbnail: cms-screen-shot.png
---
Using the Elseyworks Content Management System.

## Step 1: Log In

1. Go to **[elseyworks.com/admin](https://elseyworks.com/admin)**
2. Click **"Login with GitHub"**
3. If prompted, authorise the app on GitHub
4. You'll land on the Decap CMS dashboard

## Step 2: Create a New Post

1. In the left sidebar, click on the collection you want to add a page to
    - The **"Travel Blog"** collections are for Nick
    - The **"Articles"** collections are for Lynn's content.
    - See Nick if you need a new collection to be created.
2. Click the **"New..."** button (top right) to create a new page, or click on one of the existing pages to edit. 
3. The page editor will open

## Step 3: Fill In the Post Details

At the top of the editor you'll see several fields:

| Field | What to enter |
| --- | --- |
| **Title** | The title of your page, e.g. "A Weekend in Verona" |
| **Description** | A short description of the aerticle or post. This text will be used on the category listing page (e.g. [categories/food-travel/](/categories/food-travel/) ) |
| **Date** | The date of the post — click to get a date picker. Defaults to the current date and time. |
| **Thumbnail Image** | Select a thumbnail image to be used on the listing page. This can be one of the images used in the body. |
| **Draft** | Leave ON (true) while writing, turn OFF when ready to publish to the live site. |
| **Aliases** | Alternate URLs to this page. You can generally leave this blank for new pages. |

## Step 4: Write Your Content

The large area below the fields is the **body editor**. It works like a basic word processor when the toggle is in Rich Text mode:

- **Bold** — highlight text and click B
- **Italic** — highlight text and click I
- **Headings** — click the H1/H2/H3 dropdown
- **Links** — highlight text and click the chain icon, paste the URL
- **Images** — click the image icon, then "Choose an image" to upload from your computer (see below)

> 💡 **Tip:** You can toggle between the rich text editor and raw Markdown using the button in the top-right of the body editor. Use rich text for normal editing.

## Step 5: Images

You can insert either a regular image or a floating (text wrapped) image using the **+** button on the editor tool bar. This brings up the Images pop-up window. In this window you can:

- Upload images from your computer (one at a time)
- Select an iamge to be inserted at the current location in your content.

Once an image has been selected, you will see a "Image" or "Float Image" panel inserted into your text in the editor, and the image previewed on the right.

## Step 6: Save a Draft

At any point while writing, click **"Save"** (top right). This saves your work without publishing it. The post will be marked as a draft and won't appear on the live website yet.

You can come back and continue editing later — just click the post title in the Travel Blog list.

## Step 7: Preview Your Post

Click the **"Preview"** toggle (eye icon, top right of the editor) to see roughly how your post will look. Note this is an approximation — the live site may look slightly different.

## Step 8: Publish

When you're happy with the post:

1. Find the **"Draft"** toggle in the post fields at the top
2. Switch it to **OFF** (false)
3. Click **"Publish"**

This commits the post to GitHub. Within about **2 minutes**, GitHub Actions will automatically rebuild the site and your post will appear live at **<https://elseyworks.com>**.

## Things to Remember

- ✅ **Draft = ON** means the post is hidden from the public
- ✅ **Draft = OFF** means the post is live
- ✅ Images you upload go into the page's "bundle folder" automatically
- ⚠️ After publishing, allow **up to 2 minutes** for the site to rebuild before the post appears live

---

## Something Went Wrong?

| Problem | Solution |
| --- | --- |
| Can't log in | Make sure you're using your GitHub account |
| Post not appearing after publish | Wait 60 seconds and hard-refresh (Cmd+Shift+R) |
| Image won't upload | Check file is JPG or PNG and under 10MB |
| Accidentally published | Edit the post, set Draft back to ON, and Save |

---

Last updated: April 2026
