import { driveImage } from "@/lib/drive";

export const programaPlayaOrganizadaContent = {
  list: {
    title: "PROGRAMA PLAYA ORGANIZADA (PPO)",
    layout: "carousel" as const,
    items: [
      {
        title: "Zona segura de bañado",
        descriptionHtml:
          "<p>Zona segura de bañado, se delimita con dos banderas —combinada de roja y amarilla— donde inicia y termina la zona más segura para que los bañistas disfruten del mar, con la supervisión de guardavidas.</p>",
        image: driveImage("1VH9QI5RXZCBPaadZIhht5lDjB936oYNq", "Zona segura de bañado delimitada con banderas", 800),
      },
      {
        title: "Línea de supervivencia",
        descriptionHtml:
          "<p>Línea de supervivencia, mecate con boyas y anclaje a los lados. Esto va a permitir que cuando una persona es jalada por una corriente de resaca, tenga una última línea de flotación donde agarrarse mientras espera el rescate. Ya se colocó la primera en junio 2024.</p>",
        image: driveImage("1YSAMeYTwucueIpraYSs2bBnkwKFMqAw9", "Diagrama de línea de supervivencia en zona de resaca", 800),
      },
      {
        title: "Mapeo de la zona",
        descriptionHtml:
          "<p>Mapeo de la zona, con dron.</p><p>Límites claros del aérea total a organizar con los accesos —peatonales y vehiculares—Marcar los socios locales —todo hotel, aribnb, resta, etc— en el</p><p>aérea.</p>",
        image: driveImage("1xzTD5tgxhEOfWYDwtSn41Ncy7Ljaj1mU", "Mapa aéreo anotado de la zona del PPO", 800),
      },
      {
        title: "Socios Locales",
        descriptionHtml:
          "<p>Dentro de la zona delimitada, se contacta a todos los socios.</p><p>Ellos son la única razón de que el proyecto tenga éxito y sostenibilidad. Ellos ayudan a financiar, se comprometen con el equipo: sacarlo y meterlo todos los días. Solo esta acción de 10 – 15 minutos salva vidas.</p><p>Se comprometen a capacitar parte del personal como guardavidas y prestadores de RCP y primeros auxilios.</p>",
        image: driveImage("1aQ2FQmon84aptRPO9YSZCdsGwpxkNfn8", "Reunión con socios locales del PPO", 800),
      },
      {
        title: "Estaciones de Salvamento.",
        descriptionHtml:
          "<p>Estructuras fijas, en la playa con implementos de flotación para rescate: tubos y torpedos de rescate, caja de mecate (200metrs), salvavidas, chaleco y silbato. Compromiso con socios locales de poner y sacar cada día los implementos —al amanecer y atardecer—. Esto permite que si una persona es arrastrada por el mar, cualquier persona que este cerca tenga elementos de emergencia y flotación para el rescate.</p>",
        image: driveImage("12BU5SWqaVkMbrmTr7r0rzPzX8d_pOXTs", "Estación de salvamento con implementos de rescate", 800),
      },
      {
        title: "Plan de Emergencia",
        descriptionHtml:
          "<p>Plan de emergencia/ grupo de emergencia rápida.</p><p>Plan de emergencia con los socios locales, para toda eventualidad.</p><p>Plan se activa con el silbato u otro llamado.</p><p>Se activa el protocolo para 911 y para que socorristas acudan a la emergencia.</p><p>EDS, mecates fijos y DEA en la zona.</p><p>Puntos de ingreso y extracción, etc.</p>",
        image: driveImage("1NSEcKhzLHu_FuCXhog9SFYxpLsIzrFDM", "Plan de emergencia del PPO", 800),
      },
      {
        title: "Curso de guardavidas, RCP y primeros auxilios",
        descriptionHtml:
          "<p>Curso de guardavidas, RCP y primeros auxilios para empleados de los hoteles y negocios de la zona.</p><p>Es fundamental que todos los negocios tengan algunos (3-4) personas certificadas en RCP y primeros auxilios y 1 o 2 de guardavidas. Ya que si hay una emergencia (un ahogado en el mar o electrocutado en el hotel) siempre van a saber cómo reaccionar para que la víctima tenga más posibilidades de sobrevivir hasta que llegue la ambulancia.</p>",
        image: driveImage("1GIzctCTWsOK2__RQv_3G6NJkMH7zW5u7", "Curso de RCP y primeros auxilios para negocios locales", 800),
      },
    ],
  },
  mapImage: driveImage("15__XRaXHC0txIj3gwclsBjv7VkdmccwF", "Mapa base anotado del área del Programa Playa Organizada", 1600),
};
