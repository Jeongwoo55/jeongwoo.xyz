---
title: My experience self hosting
date: 2025-11-08
---
## Intro
Hello! My name is Jon. This is my first proper blog post. I am interested in technology, transit, photography, cities, and video games. Today, I will be writing about self hosting.

> Note: this is not a tutorial. Please see other resources if you want a step-by-step guide.

## What is self hosting?
From Wikipedia:
> Self-hosting is the practice of running and maintaining a website or service using a private web server, instead of using a service outside of the administrator's own control.

This means, you are running a piece of software on your own computer and that software is providing a website or service.

Some common self hosted software includes photo backup services, VPNs, password managers, ad blockers, media libraries, and file servers.

There is a lot of free, high-quality software created and maintained by the open source community. Sometimes, these software are better than typical services provided by Google, Microsoft, Apple, and other companies.

See https://github.com/awesome-selfhosted/awesome-selfhosted and https://selfh.st/apps/ for a list of software.

## Why should you self host?
Privacy is one of the biggest reasons why people self host. When you use a Google or Apple service, you are relying on trust to protect your data. You trust the company's reputation, privacy policy, and engineers to store your data safely and use it properly.

When you self host an open source project, you trust the contributors, security audits, and yourself. There are always privacy and security risks involved when using any online service, but self hosting allows you to control some of those risks. You can choose whether to host on LAN or the internet. Choosing the latter adds significant risks, and using an insecurely hosted application can be worse than using an application hosted by Google. You should proceed with caution.

> Note: when you self host an open source project, you can always look at the codebase to ensure privacy and security, but you should consider two things. You need to be a security expert, and you must *actually* read the entire codebase...

Cost is another reason why people self host. When you use an online service, you are paying with your data or a monthly subscription ranging from a few dollars to $15 per service. These subscriptions add up quickly and, [according to DCN](https://digitalcontentnext.org/blog/2025/08/07/q2-2025-digital-subscription-tracking-report/), average total monthly household spending on digital subscriptions is $149.64 in Q2 2025. When you self host, you are either paying for a [VPS](https://en.wikipedia.org/wiki/Virtual_private_server) (starting at $5) or buying/using an existing computer and paying electricity and internet.

Using an old computer is a great way to get started with self hosting. My first home server was an old [Dell All-in-one](https://www.pcmag.com/reviews/dell-inspiron-23-2350) which used a mobile processor. There is no need for powerful systems to self host.

Lastly, self hosting is a great way to learn and become familiar with sysadmin, networking, and Linux CLI.

## What should you self host?
There are many pieces of software which can be self hosted. Here is a list of essential and fun applications to host.

### File server
One of the first things I self hosted was a file server. File servers allow you to access files on a storage drive connected to your server from anywhere on your network. For example, you can upload photos to the file server from your phone and access it on your laptop without using any storage on your devices.

[Samba](https://www.techrepublic.com/article/how-to-set-up-quick-and-easy-file-sharing-with-samba/) is an older file server software that is simple and works well with Windows. However, it lacks a web UI and other features.

[ownCloud](https://owncloud.com/news/lifehacker-how-to-set-up-your-own-private-cloud-storage-service-in-five-minutes-with-owncloud/), [Nextcloud](https://nextcloud.com/home-users/), [Seafile](https://manual.seafile.com/latest/) and [File Browser](https://filebrowser.org/installation) are newer file server software. In my experience, these applications provide more features than I need. I have tested a few of these applications but not all of them. I would recommend seeing what makes sense for your use case.

> Note: File Browser is in "maintenance-only mode" meaning that the maintainers of the project are only providing security updates. No new features will be added. See [here](https://github.com/filebrowser/filebrowser/discussions/4906).
>
> Also note: you should always follow the [3-2-1](https://www.backblaze.com/blog/the-3-2-1-backup-strategy/) backup plan for any photos or files.

### Syncthing
[Syncthing](https://github.com/syncthing/syncthing) is an application that allows for peer-to-peer file synchronization. Using Syncthing along with a file server can replace the need for services like iCloud. I use Syncthing to sync my screenshots and download folders between my phone and computer and back up photos from phone to my server. Syncthing relies on a discovery server to find peers. You can self-host the discovery server, but the Syncthing project also maintains a public global discovery cluster.
### Immich
[Immich](https://docs.immich.app/overview/quick-start/) is a popular application that aims to replace Google Photos. It allows you to upload photos, create albums, search photos, face recognition, and other features found in Google Photos.

This software allows you to easily view photos on your server and also backup photos from your phone. Currently, I use this application to view photos from my DSLR camera which I store on my server, and my dad uses this to back up the photos on his phone.

There is a demo instance here: https://demo.immich.app/

> Note: you should always follow the [3-2-1](https://www.backblaze.com/blog/the-3-2-1-backup-strategy/) backup plan for any photos or files.

### Vaultwarden

[Vaultwarden](https://github.com/dani-garcia/vaultwarden) is "an alternative server implementation of the Bitwarden Client API, written in Rust and compatible with official Bitwarden clients." This means you can use the official Bitwarden app and browser extensions with your self hosted Vaultwarden service.
### WireGuard

[WireGuard](https://www.wireguard.com/) is a VPN protocol that can be used to connect to your home's LAN. This is useful if you do not want to expose your applications to the internet but want to access your services away from home. You can use [wireguard-tools](https://www.wireguard.com/quickstart/) or other WireGuard implementations such as [PiVPN](https://github.com/pivpn/pivpn).

> Note: PiVPN is maintained on a best-effort basis. See [here](https://github.com/pivpn/pivpn/releases/tag/v4.6.1).
### Minecraft Server

Open source software aren't the only things you can self host. You can also host game servers such as Minecraft, Factorio, or Terraria. There are many guides on self hosting via CLI or you can use a game server management software like [Pterodactyl](https://github.com/pterodactyl/panel).

## Conclusion

Self hosting is a fun way to improve your privacy and save money. It also provides additional life to your old computers and a playground to become familiar with Linux. You can self host software alternatives to Google services or other helpful services. I recommend anyone interested in technology and tinkering with Linux to give self hosting a try.