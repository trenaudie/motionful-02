Iconify API is an open source hosted (or self-hosted) service for developers.

What is it for?

API provides icon data, which made it possible to create Iconify icon components that load icons demand.
API generates SVG, which developers can link to in HTML or stylesheet.
API generates CSS to render icons as background or mask images.
API has a search engine for hosted icons, which can be used by icon pickers. Currently used by Iconify plug-ins for various UI design tools.
API can be used to offer hundreds of thousands of icons in website builders or theme customisers. Host your own API, use API's search engine in custom icon picker to allow users select icons, use icon components in UI to render icons.

Hosting API
You can host your own Iconify API service.

By hosting Iconify API yourself you:

Have full control over servers instead of relying on third party service.
Can choose which icon sets to host or host your own icon sets.
See hosting Iconify API for more details.

API is available on:

GitHub - you can customise it before deploying.
NPM - can be embedded in an app without running a full server.
Docker - for quick deployment.
Public API
Iconify project offers public API servers, which host over 200k icons from more than 150 open source icon sets.

To improve loading times, API is hosted on multiple servers in different parts of the world. Icons are usually loaded within fraction of a second.

Public API is available at https://api.iconify.design.

It is a public service, servers are free to use, but please do keep in mind that running those servers is not free. If you are using public API or API software, please consider supporting Iconify to help out with infrastructure, development and maintenance costs.

Redundancy
Sometimes there are problems with internet connections. It happens. Maybe server has issues, maybe visitor's ISP has issues.

In case main API host cannot be reached, Iconify public API has backup host names:

https://api.simplesvg.com
https://api.unisvg.com
Each of backup host names points to half of API servers. For example, in western Europe there are currently 2 servers: in Frankfurt and in London. Main host points to both, one of backup hosts points to server in Frankfurt, another backup host points to server in London. If server in Frankfurt goes down, users that are using that server can be redirected to server in London using one of backup host names.

Redundancy built in Iconify icon components accounts for that. It tries to connect to main host first, then, if there was no response in reasonable time (timeout is 0.75 seconds), it attempts to connect to one of backup hosts, then to another backup host. Small delay caused by check only affects first query, all further API queries are sent to host that responded.

See building redundant API for more details.

Queries
Iconify API can be used to render SVG, to retrieve icon data, to browse and search icons.

For full list of supported queries, their parameters and API responses see Iconify API queries documentation.

Iconify API queries
This tutorial is for developers that want to create their own tools to access Iconify API.

Iconify API supports the following basic queries:

/{prefix}/{icon}.svg dynamically generates SVG.
/{prefix}.css?icons={icons} dynamically generates CSS for icons.
/{prefix}.json?icons={icons} retrieves icon data.
/last-modified?prefixes={prefixes} returns last modification time of requested icon sets, which can be used to invalidate old icon data cache.
If list of icons is enabled, custom icon pickers can use the following queries to browse icons:

/collections returns list of available icon sets.
/collection?prefix={prefix} returns list of icons in an icon set.
If search engine is enabled, icon pickers can implement search functionality using these queries:

/search?query={keyword} returns list of icons that match keyword.
/keywords?prefix={keyword} or /keywords?keyword={keyword} returns list of keywords that contain requested keyword, which can be used for autocomplete.
Maintenance queries:

/version shows API version as plain text, unless disabled. If you are running multiple API servers, like public Iconify API does, this can be used to check which server visitor is connected to.
/update updates icon sets from its source without restarting API. This can be used to automatically keep API up to date using GitHub hooks or similar methods.
API versions
In code samples some queries above are marked as API v2, some as API v3.

Differences:

API v2 queries existed since version 2 of Iconify API, but were not documented. They are supported and will continue being supported, but at some point improved v3 versions of same queries can be added.
API v3 queries are available since version 3 of Iconify API.
You can use both versions at the same time. Improved versions of old queries might be added to solve various issues, but no need to switch to new version right away, old versions will continue to be supported.

API even supports v1 queries that aren't documented and should not be used. They are supported because they can still be found in some legacy applications, such as older versions of Iconify plug-in for Sketch.

Common parameters
All queries that return JSON data have one common parameter:

pretty is used to format JSON data, making it easy to read. Set to 1 or true to enable.