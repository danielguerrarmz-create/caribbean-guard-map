import type { Metadata } from "next";
import RichTextSection from "@/components/sections/RichTextSection";
import ListSection from "@/components/sections/ListSection";
import { nuestroTrabajo1Content } from "@/content/nuestro-trabajo1";

export const metadata: Metadata = {
  title: "Nuestro Trabajo",
  description:
    "El trabajo de Caribbean Guard: educación en seguridad acuática, capacitación continua, iniciativas de seguridad en playas y el Centro Acuático de Alto Rendimiento.",
};

export default function NuestroTrabajo1Page() {
  return (
    <>
      <RichTextSection theme="black" html={[nuestroTrabajo1Content.hero.heading]} />
      <ListSection
        theme="white"
        title={nuestroTrabajo1Content.list.title}
        layout={nuestroTrabajo1Content.list.layout}
        items={nuestroTrabajo1Content.list.items}
      />
    </>
  );
}
