---
title: Setting up my home server
date: 2026-06-28
---
## Intro

In April, I mentioned [my plan for my new home server](https://jeongwoo.xyz/blog/planning-my-home-server.md). Initially, the new home server was a nice-to-have upgrade. However, it soon became a necessity. After slightly more than 5 years of operating, the 1TB SATA SSD in my Dell AIO died... Conveniently (for Samsung), the warranty on my SSD is exactly 5 years.

However, I had some fortune on my side as I had set up [backrest](https://github.com/garethgeorge/backrest) a few weeks prior to the SSD failure. It included most files that were on the SSD. 

## Searching for cheap hardware, getting broken hardware

As a *normal* person would, I went to the April [Belton hamfest](https://tarc.org/hamexpo/) in search of a mini PC. Hamfests usually sell radios and electronic components, so I knew it might not be possible to find a mini PC. However, I found one booth that was selling computers. He did not have a mini PC ready to sell, but he did find an HP EliteDesk in his bins. We did not know the specs but he offered to give me the PC with a $50 IOU if I'm able to get the computer to work.

![SSD with screw mark](https://jeongwoo.xyz/blog/setting-up-my-home-server/belton-hamfest-pc-damaged-ssd.jpg)
Why is there a screw hole in the SSD cover...

Unfortunately, the computer did not work. This computer normally has a dedicated GPU but someone removed the GPU and left the heatsink. Then, the heatsink was screwed into the SSD. I was able to salvage two 8GB DDR4 SODIMM modules and I might be able to use the CPU (AMD Ryzen 7 Pro 4750 GE) in the future. Maybe with a new SSD, this computer will work but I was unable to enter the BIOS so I'm not sure.

![Mini PC from Belton hamfest disassembled](https://jeongwoo.xyz/blog/setting-up-my-home-server/belton-hamfest-pc-disassembled.jpg)
I was surprised to see the heatsink for the GPU

## The search continues

A few weekends later, I went to the [Vintage Computer Festival Southwest](https://www.vcfsw.org/) in DFW but the computers were much older than what I was looking for. At least it was fun seeing vintage computers and buying coffee table books.

![VCF coffee table books](https://jeongwoo.xyz/blog/setting-up-my-home-server/vcf-coffee-table-books.jpg)
The Macintosh Plus Owner's Guide and Macintosh Reference

A few more weekends later, I went to the [DFW Hamfest](https://www.dfwhamexpo.com/) where I met the same computer booth owner from Belton. Lucky for me, he brought two mini PCs and two 256GB SSDs for me. While I offered to pay, he insisted I take it for free and pass on the generosity. 

![DFW hamfest haul](https://jeongwoo.xyz/blog/setting-up-my-home-server/dfw-hamfest-haul.jpg)
My haul from the DFW hamfest

After inspecting the mini PCs, I found that both did not have RAM and one unit was missing a CPU. But, I was able to build a working PC using the computer with CPU, RAM from the initial PC, and a 1TB SSD given as a gift from a friend. Once the computer booted, I started installing Linux.

## Setting up my home server

![New home server](https://jeongwoo.xyz/blog/setting-up-my-home-server/new-home-server.jpg)
My new home server!

At first, I tried to install Ubuntu but ran into a weird boot issue where the screen would go blank. Debian also had the same issue but I was able to SSH into the computer.

> Sidenote: why is the Ubuntu server installation script worse than Debian or even Arch... Maybe I did something wrong, but Debian was super straightforward and better than Ubuntu installation.

For now, I moved most of my Docker applications to the new server. I am trying out [Arcane](https://github.com/getarcaneapp/arcane) as my Docker management software. So far, it's okay. The dashboard is a little glitchy.

In addition to Arcane, I am also trying out [Cloudflare Access](https://www.cloudflare.com/sase/products/access/), as suggested by a friend. It's nice to add an additional layer of protection for my self hosted apps especially with the rise of security risk from AI.

For next steps, I still need to set up a DNS, Minecraft/game servers, NAS, Immich, and better networking/security. Besides better security, these other items can wait a bit longer. Also, I want to get another mini PC and set up a cluster and a 10in rack. Maybe stay tuned for part 3 in a few months time or whenever computer parts become cheaper.

## Conclusion

TL;DR, go to hamfests to get free (maybe) working hardware and turn that into a home server.