import type { RichImage } from "./content-types";

export function driveImg(fileId: string, width = 1600): string {
  return `https://lh3.googleusercontent.com/d/${fileId}=w${width}`;
}

export function driveImage(fileId: string, alt: string, width = 1600): RichImage {
  return { url: driveImg(fileId, width), alt };
}
