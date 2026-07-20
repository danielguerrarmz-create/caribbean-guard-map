import { driveImage } from "@/lib/drive";

export const homeContent = {
  hero: {
    backgroundImage: driveImage(
      "1Aj-tHA9_LlbWY5RdS0B0Xh3yChTjQXpk",
      "Guardavidas de Caribbean Guard patrullando la playa",
      1920,
    ),
    overlayOpacity: 0.15,
    heading: '<h1 style="white-space:pre-wrap;">Caribbean Guard: Salvando Vidas</h1>',
    button: { text: "Únete", link: "/involcrate" },
  },
  video: {
    title: "PROGRAMA PLAYA ORGANIZADA",
    driveEmbedId: "1PW6EDWxp3KMMNC41IjFOeWyBjzvXvrSb",
  },
  mission: {
    html: [
      '<h2 style="text-align:center;white-space:pre-wrap;">Nuestra misión</h2>',
      '<p style="white-space:pre-wrap;"><strong>Misión:</strong> Revolucionar la seguridad acuática en el Caribe Sur y cambiar el paradigma de los incidentes por ahogamiento.</p><p style="white-space:pre-wrap;"><strong>Visión:</strong> La soberanía y gestión de la seguridad acuática debe estar en manos de la comunidad, siendo la única opción para que sea sostenible. Si creamos una comunidad fuerte en el agua, vamos a reducir los incidentes acuáticos.</p><p style="white-space:pre-wrap;">Nuestro objetivo principal es desarrollar y crear una comunidad que se sienta segura y sea fuerte en el agua. Enseñando y entrenando técnicas de salvamento, natación y apnea; con nuestros tres clubes buscamos reducir los ahogamientos y crear “embajadores locales” que puedan prevenir emergencias.</p><p style="white-space:pre-wrap;">La columna vertebral de nuestra organización es la educación continua, ofreciendo cursos y formando: Guardavidas, instructores de RCP y primeros auxilios, instructores de natación y de freediving, que a su vez enseñan a la comunidad. Estos esfuerzos aseguran que los miembros de la comunidad sean más seguros en el agua. También buscamos desarrollar programas como la iniciativa Bandera Roja y Amarilla para playas organizadas y la guardia móvil. Nuestro objetivo final es establecer un Centro Acuático de Alto Rendimiento en el Caribe Sur que unifique todas las actividades relacionadas con el agua, comenzando por enseñar a la comunidad a flotar y nadar, y asegurarnos que el CADAR financie a la organización para ser autosuficientes.</p>',
    ],
  },
};
