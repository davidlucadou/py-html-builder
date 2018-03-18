# Python HTML builder

Generates static HTML pages from a list of given files.

This program uses a JSON file to append HTML files so you can easily reuse elements and regenerate pages with newer versions without depending on iframes, JavaScript, or a CMS. Instead, you can run an extremely lightweight webserver that has static HTML files, with far lower maintenance times when you need to update common elements, especially headers, meta tags, and footers.

### Why should I use this instead of using common JavaScript or iframes?

When you depend on JavaScript for page navigation or inserting content, you destroy the ability of text-only web browsers and users with JavaScript disabled to navigate your site. Iframes are old and difficult to scale for different devices (and even resized browser windows), and are generally considered bad practice. In addition, iframes might not be rendered in text-only browsers suchs as Links.
Reducing your dependency on these will also decrease load times and make your code easier to maintain. A snappy website is a happy website. JavaScript should be used for animations and polish, not basic navigation, but I see far too many websites toss NoScript compatibiliy out the window and have slow to render pages.

### Can I see an example of a website that uses this?

Sure, go to https://www.monotonetim.tv (this isn't my personal site, I built it for a Twitch streamer). You might notice if you paste this link in Slack, the link preview displays the stream status for the Twitch streamer MonotoneTim. JavaScript isn't executed by link unfurlers, so I built this program to generate a new version of the site whenever he started or stopped streaming, and push it to S3. I'll be publishing it as well once I clean the code up a bit more.

## How do I use this?

Usage: `python3 html-gen.py [configfile.json]`

### Ok, what do I put in the json file?

Check out the files in docs. timbuild.json is the actual config file I use for https://www.monotonetim.tv.

### The Structure of the JSON file:

```json
{
  "content-root": "[the path to the individual files to assemble]",
  "webserver-root": "[the path to write the assembled HTML files]",
  "pages": [
    { "path": "[the path this file will reside in inside the webserver-root]",
      "lang": "[the language of the page, to be used in <html lang=\"__\">]",
      "content": {
        "header": {
          "0": "[the first file to append, with paths relative to content-root]",
          "1": "[the second file to append]",
          "2": "[etc.]"
        }, "head": {
        }, "body": {
        }
      }
    },
    { "path": "[the second webpage]",
      "lang": "[the language]",
      "content": {
        "header": {
        }, "head": {
        }, "body": {
        }
      }
    }
  ]
}
```

It's easy to extend by adding in more pages. Because you can break common elements into individual files, it is extremely easy to make custom error pages and build them, without worrying about having to go through every file to update elements.
Since HTML files are just appended, you could base64 encode images into the HTML and that'll end up in the source files, but really this is just intended to build the HTML files.

#### FAQ

> Does this also copy all my images, videos, etc. into one place?

No, but that is a higher priority item. The original idea behind this was to generate just HTML files so I would have a directory of a few files that I could push onto S3 (which charges $0.005 per 1,000 non-GET requests every month, so reducing the number of PUTs saves money).

> Does this require a particular webserver?

No. You can use this with any webserver, even going to an HTML page hosted locally in your browser or pushing it onto S3 like I do.
