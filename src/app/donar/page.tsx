import type { Metadata } from "next";
import RichTextSection from "@/components/sections/RichTextSection";
import { donarContent } from "@/content/donar";

export const metadata: Metadata = {
  title: "Donar",
  description:
    "Dona a Caribbean Guard: transferencia bancaria, PayPal o Sinpe Móvil para apoyar la seguridad acuática en el Caribe Sur de Costa Rica.",
};

export default function DonarPage() {
  return (
    <RichTextSection
      theme="bright"
      html={donarContent.intro.html}
      image={donarContent.intro.image}
      buttons={[donarContent.intro.button]}
    />
  );
}
