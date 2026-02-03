# BCn (Block Compression) & You

This file tries to explain texture compression formats used by XIV in a practical and relatively short way. If you want more technical information [this Wikipedia article is a good read](https://en.wikipedia.org/wiki/S3_Texture_Compression).

[This article by Nathan Reed on the topic of BCn compression](https://www.reedbeta.com/blog/understanding-bcn-texture-compression-formats/) is also a very good and detailed read if you are interested in the topic.

[This spreadsheet by Sel](https://docs.google.com/spreadsheets/d/1kIKvVsW3fOnVeTi9iZlBDqJo6GWVn6K6BCUIRldEjhw/edit?ref=xivmods.guide&gid=1406279597#gid=1406279597) is also a useful resource when talking about XIV textures and what information is stored in each of their channels. If you haven't yet, it's worth bookmarking or saving it somewhere, you will probably come back to it!

## Formats

Block compression refers to the different types of compression that can be used in .DDS texture files. These are all lossy compression formats, meaning some data is thrown away when compressing the images, leading to some quality loss.

Block Compression formats (BCn) currently range from BC1 to BC7.

- **BC1 (DXT1):** Low quality color data, 1-bit alpha (on/off).
- **BC2 (DXT3):** Low quality color, 4-bit alpha (better than BC1, sharp alpha use cases).
- **BC3 (DXT5):** Low quality color, interpolated alpha (better than BC2, smooth alpha gradients).
- **BC4:** 1 Greyscale channel compressed with higher quality.
- **BC5:** 2 Greyscale channels compressed with higher quality.
- **BC6H:** Color compression used for HDR images.
- **BC7:** Similar to BC3 but much better compression and heavier on the GPU.

Looking at these specs you will see that some of these formats are not as relevant to us in XIV.

- We have no use for BC6H and its HDR capabilities.
- In XIV as far as I know, we also have no use for BC4 which compresses only one channel and discards everything else.
- We can mostly discard BC2 which has a more specific use case for sharp alpha textures. BC1 should be good enough for lower quality textures when no alpha is needed, and BC3 when alpha is needed.

## BC5 & BC7

All of this leaves us with BC5 & BC7. So let's compare the two a bit more and see when BC5 can help.

Like we've said before, BC7 is a pretty good compression algorithm, it has very little image quality loss for color information like diffuse maps, and small compression artifacts are much less noticeable on color textures in-game. However, BC7 is a bit more limited for data textures packed into one file such as the mask texture because of channel interference.

<!-- TODO: Add BC7/Uncompressed Image comparison. -->

Because of this, it kinda falls short is with normal maps. Remember that normal maps are not just color information, they represent vector data for a 3D model. Imagine an arrow coming out of each pixel in the normal map and pointing in a slightly different direction. Texture compression artifacts that wouldn't be all that noticeable when examining the texture with our eyes might still cause problems in-game, and this is usually even more obvious on shinier or metallic surfaces.

This is where BC5 can help a bit. BC5 uses the same amount of data on 2 channels (red and green) as BC7 uses in 4 (red, green, blue & alpha), which results in better image quality at the same file size, and the two channels are compressed separately. The blue channel in normal maps can be safely discarded and rebuild at run time, so the red and green channels in a BC5 are all we need.

<!-- TODO: Add BC5/BC7 Image comparison. -->

Another texture file where BC5 is a better option than BC7 is ID maps, since these also store information in only the red and green channels. Saving this in BC7 would be a waste since the blue and alpha channels aren't going to be used.

## When to avoid BC5

But of course, there's a catch. In XIV we sometimes pack an opacity channel in the blue channel of the normal map texture. If we need to store an opacity channel, BC5 is no good to us.

⚠️ Saving a normal map with opacity data in the blue channel would save only the normal map (red and green channels) and discard the rest!

## Guidelines / TL;DR

Keep in mind this topic can be a bit subjective, not in how the compression works, but on how your textures look in the end, and while I'm trying to give good advice, it's up to you to decide what's best for your mods.

- For the best image quality uncompressed textures (RGBA8) can't be beaten, but be reasonable, specially if your textures are 4K, chances are you aren't gaining much at all by avoiding compression.

- One uncompressed 4k texture goes from 85MB to 21.25MB when compressed as BC5 or BC7.

- Use BC5 when possible, like in _id maps and other textures that **only need the red and green channel**, like normal maps without opacity. This will be a quality gain over BC7.

- If you are worried about compressing your normal maps because of fine detail like fabric patterns, keep in mind that XIV materials support tileable detail maps and you can control their opacity, mipmap bias, sharpness, etc per colorset row, so this option can look better (regardless of compression), but  will also allow you to keep clean detail on normal maps without sacrificing compression.

## Compression Recommendations by Texture Type

- Diffuse: BC3/BC7 depending on required image quality.
- ID: BC5.
- Mask: BC7, Uncompressed if artifacts are noticeable.
- Normal Map: BC5 if no Opacity needed, BC7 otherwise. Uncompressed if you can notice any compression artifacts after trying BC5/7.

## Compression Default Settings in Substance to XIV

In order to error on the safe side, the plugin's defaults lean a bit more towards quality than then recommendations above.

- Diffuse: BC7.
- ID: BC5.
- Mask: BC7.
- Normal Map: Uncompressed.

While any amount of compression, regardless of the format, will lead to some image quality loss, it's up to you to determine how clean your textures need to look and what resolution they need to be in. Maximizing the texture space when making your UVs is also very important.

I would still recommend that you check for texture quality and re-export with different formats, since that's part of the point of the plugin, being able to do quick texture exports, see things in game, compare, and fine tune things more easily!

## Conclusion

If you are here I'll assume you care about texture authoring in XIV in one way or another. This topic is tied to the Substance to XIV plugin, and I feel a lot of people that make mods for the game haven't looked into the differences between the available formats, and therefore when it's best to use one or another.

While uncompressed textures will always look better, the image quality impact is in many cases negligible, unless you are zooming in on the texture itself to see the differences, and especially at higher resolutions like 4k, where a single uncompressed texture will take 85MB, up to four times the size of a compressed one. Multiply that by (usually) 3 textures per gear piece, and several gear pieces per mod, several mods on screen, not to mention hundreds of them installed on your SSD, and you can see where this is going. Bit by bit it becomes a considerable waste of VRAM and storage resources for little to no gain.
