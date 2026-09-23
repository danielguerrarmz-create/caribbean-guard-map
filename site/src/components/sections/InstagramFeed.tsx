"use client";

import Image from "next/image";
import { useEffect, useState } from "react";
import type { Theme } from "@/lib/content-types";

type BeholdPost = {
  id: string;
  permalink: string;
  mediaType: "IMAGE" | "VIDEO" | "CAROUSEL_ALBUM";
  caption?: string;
  sizes: {
    small: { mediaUrl: string; width: number; height: number };
    medium: { mediaUrl: string; width: number; height: number };
  };
};

type BeholdFeedResponse = {
  posts: BeholdPost[];
};

type InstagramFeedProps = {
  feedUrl?: string;
  theme?: Theme;
  count?: number;
};

const INSTAGRAM_PROFILE_URL = "https://instagram.com/caribbeanguard";

export default function InstagramFeed({
  feedUrl,
  theme = "white",
  count = 6,
}: InstagramFeedProps) {
  const [posts, setPosts] = useState<BeholdPost[] | null>(null);
  const [failed, setFailed] = useState(false);

  const resolvedUrl = feedUrl ?? process.env.NEXT_PUBLIC_BEHOLD_FEED_URL;

  useEffect(() => {
    if (!resolvedUrl) {
      setFailed(true);
      return;
    }

    let cancelled = false;
    fetch(resolvedUrl)
      .then((res) => {
        if (!res.ok) throw new Error(`Behold feed responded ${res.status}`);
        return res.json() as Promise<BeholdFeedResponse>;
      })
      .then((data) => {
        if (!cancelled) setPosts(data.posts ?? []);
      })
      .catch(() => {
        if (!cancelled) setFailed(true);
      });

    return () => {
      cancelled = true;
    };
  }, [resolvedUrl]);

  if (failed || (posts && posts.length === 0)) {
    return (
      <section className={`theme-${theme} bg-background text-foreground`}>
        <div className="mx-auto max-w-5xl px-6 py-16 text-center md:py-24">
          <a
            href={INSTAGRAM_PROFILE_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-3 rounded-lg border border-foreground/15 px-8 py-6 transition-colors hover:border-accent"
          >
            <InstagramIcon className="h-8 w-8 text-accent" />
            <span className="text-lg font-semibold">
              Síguenos en Instagram @caribbeanguard
            </span>
          </a>
        </div>
      </section>
    );
  }

  const visiblePosts = posts?.slice(0, count) ?? Array.from({ length: count });

  return (
    <section className={`theme-${theme} bg-background`}>
      <div className="mx-auto max-w-6xl px-1 py-16 md:px-6 md:py-24">
        <div className="grid grid-cols-3 gap-1 md:grid-cols-6 md:gap-2">
          {visiblePosts.map((post, i) =>
            post ? (
              <a
                key={post.id}
                href={post.permalink}
                target="_blank"
                rel="noopener noreferrer"
                className="group relative aspect-square overflow-hidden"
              >
                <Image
                  src={post.sizes.medium.mediaUrl}
                  alt={post.caption?.slice(0, 140) || "Publicación de Instagram"}
                  fill
                  unoptimized
                  className="object-cover transition-transform duration-300 group-hover:scale-105"
                />
              </a>
            ) : (
              <div key={i} className="aspect-square animate-pulse bg-foreground/5" />
            ),
          )}
        </div>
      </div>
    </section>
  );
}

function InstagramIcon({ className = "" }: { className?: string }) {
  return (
    <svg
      viewBox="0 0 24 24"
      className={className}
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
      aria-hidden="true"
    >
      <rect x="3" y="3" width="18" height="18" rx="5" />
      <circle cx="12" cy="12" r="4.2" />
      <circle cx="17.3" cy="6.7" r="0.6" fill="currentColor" stroke="none" />
    </svg>
  );
}
