import { driveImage } from "@/lib/drive";

export const lifesavingClubContent = {
  intro: {
    html: ['<h1 style="white-space:pre-wrap;">LIFESAVING CLUB</h1>'],
    image: driveImage("1UcBVlQzEGdVL17NLc9FPmJHCeaWogUdm", "Logo del Lifesaving Club", 800),
  },
  list: {
    title: "",
    layout: "carousel" as const,
    items: [
      {
        title: "Educación Continua",
        descriptionHtml:
          "<p>La Educación Continua es la columna vertebral de la asociación, hasta el momento, impartimos los siguientes cursos a la comunidad:</p><p>- 5 cursos de Guardavidas</p><p>- 1 curso para Instructores de RCP &amp; Primeros Auxilios</p><p>- 1 curso para instructores de natación &nbsp;</p><p>- 1 curso guardavidas Jr. Nipper</p><p>- 1 curso ELLIS de RCP</p>",
        image: driveImage("1p1pWGKu6GgP_BKFaAL6UmYxvpzYaTwPk", "Curso de guardavidas", 800),
      },
      {
        title: "Guardias",
        descriptionHtml:
          "<p>Desde la creación de la organización, hasta hoy, nunca murió nadie en nuestras guardias. </p><p>Patrullamos Playa Grande y ahora Playa Chiquita, los domingos, los días con más incidencias de ahogamiento en todo el país. </p><p>También hacemos guardias extras para Semana Santa, algunos feriados y días festivos.</p>",
        image: driveImage("15UWj_wxkj-Hzbt9xzI8gkENayDAwc6h_", "Guardavidas patrullando Playa Grande", 800),
      },
      {
        title: "Entrenamiento de Salvamento",
        descriptionHtml:
          "<p>Todos los sábados a la mañana, en diferentes locaciones —dependiendo de las condiciones del mar— se realiza un entrenamiento en el cual se ven técnicas y habilidades de salvamento, abiertos a la comunidad.</p>",
        image: driveImage("11d-LezrAv0kV7Evk6RQ44UzorpqhT59E", "Entrenamiento de salvamento acuático", 800),
      },
      {
        title: "Red de alerta de emergencias.",
        descriptionHtml:
          "<p>Tenemos un grupo de emergencias con más de 70 miembros de la comunidad —la mayoría: guardavidas, surfistas, nadadores, pescadores, buceadores, apneistas—.</p><p>En cuanto sucede una emergencia, activamos el protocolo y las personas que están cerca del incidente y pueden ayudar se acercan a colaborar en el rescate. Muchas vidas se han salvado.</p>",
        image: driveImage(
          "1MLg72IBLViHVX15kwaiDipt_AArs7Uh4",
          "Voluntarios de la red de alerta de emergencias",
          800,
        ),
      },
    ],
  },
};
