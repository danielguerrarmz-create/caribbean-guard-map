import type { Metadata } from "next";
import ListSection from "@/components/sections/ListSection";
import ImageBlock from "@/components/sections/ImageBlock";
import { programaPlayaOrganizadaContent } from "@/content/programa-playa-organizada";

export const metadata: Metadata = {
  title: "Programa Playa Organizada",
  description:
    "El Programa Playa Organizada (PPO) de Caribbean Guard organiza zonas seguras de bañado, líneas de supervivencia y estaciones de salvamento en las playas del Caribe Sur.",
};

export default function ProgramaPlayaOrganizadaPage() {
  return (
    <>
      <ListSection
        theme="white"
        title={programaPlayaOrganizadaContent.list.title}
        layout={programaPlayaOrganizadaContent.list.layout}
        items={programaPlayaOrganizadaContent.list.items}
      />
      <section className="theme-light bg-background">
        <div className="mx-auto max-w-6xl px-6 py-16 md:py-24">
          <ImageBlock
            url={programaPlayaOrganizadaContent.mapImage.url}
            alt={programaPlayaOrganizadaContent.mapImage.alt}
            className="aspect-[21/9] rounded-lg"
          />
        </div>
      </section>
    </>
  );
}
