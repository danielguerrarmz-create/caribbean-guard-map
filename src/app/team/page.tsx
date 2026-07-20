import type { Metadata } from "next";
import RichTextSection from "@/components/sections/RichTextSection";
import ListSection from "@/components/sections/ListSection";
import Accordion from "@/components/sections/Accordion";
import { teamContent } from "@/content/team";

export const metadata: Metadata = {
  title: "Team",
  description:
    "Conoce a la Familia de Mar: el equipo de guardavidas, instructores y voluntarios que hacen posible el trabajo de Caribbean Guard.",
};

export default function TeamPage() {
  return (
    <>
      <RichTextSection theme="light" html={[teamContent.heading]} />
      <ListSection theme="white" title={teamContent.cardsTitle} layout="carousel" items={teamContent.cards} />
      <Accordion theme="light" items={teamContent.accordion} />
    </>
  );
}
