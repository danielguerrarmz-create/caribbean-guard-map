export type Theme = "white" | "light" | "black" | "bright";

export type RichImage = {
  url: string;
  alt: string;
};

export type ButtonData = {
  text: string;
  link: string;
};

export type ListItem = {
  title: string;
  descriptionHtml: string;
  button?: ButtonData | null;
  image?: RichImage | null;
};

export type ListLayout = "simple" | "carousel";

export type AccordionItem = {
  title: string;
  contentHtml: string;
};
