import type { Metadata } from "next";
import HeroSection from "@/components/sections/HeroSection";
import VideoSection from "@/components/sections/VideoSection";
import RichTextSection from "@/components/sections/RichTextSection";
import InstagramFeed from "@/components/sections/InstagramFeed";
import { homeContent } from "@/content/home";

export const metadata: Metadata = {
  title: "Inicio",
  description:
    "Caribbean Guard: salvando vidas en el Caribe Sur de Costa Rica a través de guardavidas, natación, freediving y educación en seguridad acuática.",
};

export default function HomePage() {
  return (
    <>
      <HeroSection
        theme="black"
        backgroundImage={homeContent.hero.backgroundImage}
        overlayOpacity={homeContent.hero.overlayOpacity}
        heading={homeContent.hero.heading}
        button={homeContent.hero.button}
      />
      <VideoSection
        theme="light"
        title={homeContent.video.title}
        src={homeContent.video.src}
        poster={homeContent.video.poster}
      />
      <RichTextSection theme="light" html={homeContent.mission.html} />
      <InstagramFeed />
    </>
  );
}
