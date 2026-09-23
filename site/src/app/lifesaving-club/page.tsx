import type { Metadata } from "next";
import RichTextSection from "@/components/sections/RichTextSection";
import ListSection from "@/components/sections/ListSection";
import { lifesavingClubContent } from "@/content/lifesaving-club";

export const metadata: Metadata = {
  title: "Lifesaving Club",
  description:
    "El Lifesaving Club de Caribbean Guard forma guardavidas, patrulla las playas del Caribe Sur y mantiene una red de alerta de emergencias.",
};

export default function LifesavingClubPage() {
  return (
    <>
      <RichTextSection theme="light" html={lifesavingClubContent.intro.html} image={lifesavingClubContent.intro.image} />
      <ListSection theme="white" layout={lifesavingClubContent.list.layout} items={lifesavingClubContent.list.items} />
    </>
  );
}
