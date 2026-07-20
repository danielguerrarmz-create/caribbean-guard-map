import type { Metadata } from "next";
import RichTextSection from "@/components/sections/RichTextSection";
import { freedivingClubContent } from "@/content/freediving-club";

export const metadata: Metadata = {
  title: "Freediving Club",
  description:
    "El Freediving Club de Caribbean Guard desarrolla la apnea en el Caribe Sur con cursos, talleres y competencias.",
};

export default function FreedivingClubPage() {
  return (
    <RichTextSection theme="light" html={freedivingClubContent.intro.html} image={freedivingClubContent.intro.image} />
  );
}
