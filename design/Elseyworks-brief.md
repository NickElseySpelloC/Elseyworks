# Elseyworks Brief

## Objective

Create a new website - elseyworks.com - that showcases Lynn's writing and content. Make the style and presentation of the site visually compelling, engaging and professional. Maintain the existing categorisation of content and articles (food, careers, publishing, etc.).

Use your creativity to make the page design as engaging, professional and polished as possible. Feel free to add additional images and graphics where appropriate.

Where an image of a published article has been provided, continue to include this in the site. 

## Starting Point 

You will be working in the `~/dev/elseyworks` repo. This was cloned from the https://github.com/NickElseySpelloC/Elseyworld which is the repo for the Elseyworld.com website. Elseyworld currently includes a section for Lynn's content and articles (located at `content/articles`repo), as well as other content.

Elseyworld.com uses Hugo, the Congo theme and Decap CMS to manage the site content. Elseyworld.com is hosted on Github pages and fronted by Cloudflare DNS.

The Elseyworks clone (your working repo) is pointed at https://github.com/NickElseySpelloC/Elseyworks and it's been configured to use it's own Github pages. The elseyworks.com domain has also been configured in Cloudflare. 

## Implementation details

* Do not make any changes to the `~/dev/elseyworld` repo 
* Feel free to make any changes you need to your working repo  `~/dev/elseyworks`
* Remove all the content from the site that doesn't pertain to Lynn's content and articles, i.e. anything outside the current `content/articles` folder. Restructure the remainder as needed.
* Lynn's content will become the entire site. 
* Create a home page for the site.
* Once your work is complete and deployed to Github pages, Lynn will be managing the content in the future rather than me.

## Lynn's technical skills

Lynn is very not technical - dealing with Hugo, markdown files, shortcode inserts, etc. will be too much for her. 

I suggest that we find a system that makes it very easy for Lynn to manage the site going forward. Probably the ideal approach would be to configure a Claude agent that she can easily interact with. For example, Lynn would give the agent a PDF of a new article and just ask it to add it to the site. The agent would update the local site as appropriate, adding the content and giving Lynn a local URL to preview the updated site. If Lynn approves, the agent can then do the git commit and push which will trigger a Github workflow to update the live site.





