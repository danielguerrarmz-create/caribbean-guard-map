import type { Metadata } from "next";
import RichTextSection from "@/components/sections/RichTextSection";
import { nuestroTrabajoContent } from "@/content/nuestro-trabajo";

export const metadata: Metadata = {
  title: "Historia",
  description:
    "La historia de Caribbean Guard: de una guardia comunitaria de Semana Santa 2021 a una asociación con más de 70 miembros activos en el Caribe Sur.",
};

export default function NuestroTrabajoPage() {
  return (
    <>
      <RichTextSection
        theme="light"
        html={nuestroTrabajoContent.intro.html}
        image={nuestroTrabajoContent.intro.image}
      />
      <RichTextSection
        theme="white"
        html={nuestroTrabajoContent.story.html}
        image={nuestroTrabajoContent.story.image}
        imagePosition="left"
      />
    </>
  );
}
