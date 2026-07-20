import type { Metadata } from "next";
import HeroSection from "@/components/sections/HeroSection";
import Marquee from "@/components/sections/Marquee";
import RichTextSection from "@/components/sections/RichTextSection";
import { visionContent } from "@/content/vision";

export const metadata: Metadata = {
  title: "Vision",
  description:
    "La visión de Caribbean Guard: la ley de tercios entre comunidad, empresarios y gobierno para la seguridad acuática sostenible en Costa Rica.",
};

export default function VisionPage() {
  return (
    <>
      <HeroSection
        theme="black"
        backgroundImage={visionContent.hero.backgroundImage}
        overlayOpacity={visionContent.hero.overlayOpacity}
        heading={visionContent.hero.heading}
      />
      <Marquee theme="bright" text={visionContent.marquee.text} />
      <RichTextSection theme="light" html={visionContent.thirds.html} />
      <RichTextSection theme="white" html={visionContent.policies.html} />
    </>
  );
}
