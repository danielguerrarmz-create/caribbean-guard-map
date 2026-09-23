import type { Metadata } from "next";
import ListSection from "@/components/sections/ListSection";
import { proyectosContent } from "@/content/proyectos";

export const metadata: Metadata = {
  title: "Proyectos",
  description:
    "Los proyectos de Caribbean Guard: la Bodega Digna, el Programa Guardia Móvil y el Centro Acuático de Alto Rendimiento (CADAR).",
};

export default function ProyectosPage() {
  return (
    <ListSection
      theme="white"
      title={proyectosContent.list.title}
      layout={proyectosContent.list.layout}
      items={proyectosContent.list.items}
    />
  );
}
