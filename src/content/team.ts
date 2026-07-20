import { driveImage } from "@/lib/drive";

type TeamMember = {
  name: string;
  role: string;
  photoFileId: string;
  bioHtml: string;
};

const MEMBERS: TeamMember[] = [
  {
    name: "Elías Brown",
    role: "Jefe de Operaciones y Guardavidas",
    photoFileId: "1ZZ1g4-cmeIAFBMHGZ4ViR3_TAmWMRy6e",
    bioHtml:
      "<p><em>Jefe de Operaciones y Guardavidas</em></p><p>Nacido y criado en Puerto Viejo. El mar es su compañero constante, desde pequeño, ya sea surfeando, pescando, haciendo freediving o de guardavidas.</p><p>Vivió 6 años en Francia y viajó varias veces a Australia, uno de los países con mayor nivel de organización de guardavidas en el mundo, y ahí fue donde se dio cuenta de todo lo que había por hacer en el Caribe y se involucró de lleno en Caribbean Guard.</p><p>Hace varios años, cuando tenía el hostel, donó la torre de seguridad en Cocles (antes de Cruz Roja) y hace un año, donó la segunda torre de seguridad en Playa Grande para Caribbean Guard.</p><p>Ahora se dedica a la construcción y es parte fundamental de la organización.</p><p><em>“El mar, siempre es un constante recordatorio del poder sobrenatural, al cual le tengo un profundo respeto”.</em></p>",
  },
  {
    name: "Milagro Muñoz Araya",
    role: "Guardavidas, Instructora de Natación y Secretaria de la Asociación",
    photoFileId: "1Nd3rQXkaUJs4D0qB8b4fTdOecv_HX1wV",
    bioHtml:
      "<p><em>Guardavidas</em></p><p><em>Instructora de natación.</em></p><p><em>Secretaria de la Asociación.</em></p><p>Desde niña amaba nadar y participó de varios torneos de natación; en la universidad recibió una beca deportiva para competir y pudo estudiar la carrera de sus sueños, gracias al deporte.</p><p>Hace 5 años vino a vivir al Caribe a ejercer su profesión como veterinaria y se enamoró del lugar: las playas, las montañas y su gente.</p><p>Actualmente es Guardavidas Voluntaria, de Caribbean Guard donde también se recibió como Instructora de Natación y enseña, a niños de la zona, a nadar.</p><p><em>“Para mí es un placer pertenecer a este grupo de voluntarios y devolver a la comunidad,</em></p><p><em>en agradecimiento, por toda la ayuda brindada”.</em></p>",
  },
  {
    name: "Mike Geist",
    role: "Director de Educación, Instructor de Guardavidas y Entrenador de Natación",
    photoFileId: "1-eGwStYsIvdahngn6h23-4nXvLZS1MdW",
    bioHtml:
      "<p><em>Instructor de guardavidas, Coach de natación</em></p><p><em>Capitán de PPO Chiquita</em></p><p>Mike es de Colorado y vive en Punta Uva. La natación fue su pasión, toda la vida. Ex nadador competitivo, entrenador de natación de la escuela secundaria, guardavidas y nadador de rescate de combate en el Cuerpo de Marines de EE. UU.</p><p>Recientemente recibió su certificación como Instructor de Guardavidas de Surf e Instructor de RCP y EFR de la mano de Caribbean Guard y Swim Safe.</p><p><em>“Estoy emocionado de trabajar con nuestra comunidad para mejorar nuestra capacidad general de responder a emergencias, y marcar la diferencia salvando vidas en nuestras preciosas playas y sus alrededores”.</em></p>",
  },
  {
    name: "Sofía Córdoba",
    role: "Guardavidas certificada ILTP, Instructora de Instructores de RCP y EFR",
    photoFileId: "1w6hG8_-JvsO6Md9mfdkKBect16scTjnx",
    bioHtml:
      "<p><em>Guardavidas certificada ILTP, &nbsp;</em></p><p><em>Instructor de Instructores de RCP &amp; EFR by Ellis &amp; Associates.</em></p><p>Nacida en San Domingo de Heredia, es mamá y empresaria local. Vive en Puerto Viejo, desde el 2015, cuando se enamoró del Caribe y desde entonces vio la necesidad de conectarse con el mar, de forma segura. A sus 30 años aprendió a surfear con bodyboard y con Caribbean Guard aprendió a nadar en aguas abiertas a los 35; una mujer creativa, emprendedora e incansable que lucha por sus sueños. Convencida de la necesidad de crear espacios seguros para incentivar la salud y el movimiento, ha creado TRIBU, un centro de Acondicionamiento Físico en Puerto Viejo y una plataforma de entrenamiento para acompañar a hombres y mujeres a&nbsp; lograr sus objetivos de salud y bienestar, con programas de&nbsp; entrenamiento personalizados.</p>",
  },
  {
    name: "Lucas Iturriza",
    role: "Fundador y Presidente",
    photoFileId: "1UAyvPo9V4ufQK3mlUsmTuN2YTLmYCbcZ",
    bioHtml:
      "<p><em>Fundador y Presidente</em></p><p>Nació en Buenos Aires y está radicado en el Caribe Sur desde 2007 con su familia. Ha viajado extensivamente por los cinco continentes, es storyteller —fotógrafo, escritor y productor audiovisual—, emprendedor y siempre su elemento fue el agua. Ex instructor de buceo, de RCP y primeros auxilios, cambió los tanques por la apnea y pesca submarina.</p><p>Es quien aporta la visión y es “el motor” detrás de la organización.</p><p><em>“Tenemos la misión de revolucionar la seguridad acuática en nuestra comunidad, creando una comunidad fuerte en el agua y así bajar el índice de mortalidad por ahogamientos”.</em></p>",
  },
  {
    name: "Georgina De Puch",
    role: "Jefa de Patrullajes, Fundadora del Equipo de Playa Negra, Guardavidas e Instructora de Natación",
    photoFileId: "1f2WyawJ6X2eaP-NM4dd699qyzHiyrnaT",
    bioHtml:
      "<p><em>Guardavidas, Instructora de natación</em></p><p><em>Fundadora Playa Negra Team</em></p><p>Nació en Buenos Aires, y aprendió a nadar desde muy pequeña. A los 18 años, comenzó a entrenar, de forma regular, y nunca más paró.</p><p>Es veterinaria, Especialista en Cirugía de Pequeños Animales, Doctora en Ciencias Veterinarias, Docente e Investigadora.</p><p>A sus 33, conoció a sus primeros cómplices en aguas abiertas, y ahí se inicia una larga lista de experiencias increíbles, que la lleva a querer ser guardavidas. Después de 3 años de mucho entrenamiento, logró su objetivo y se graduó como guardavidas profesional con 39 años, en Argentina.</p><p>Sus planes de vida cambiaron cuando dijo que ya no podía vivir más lejos del mar.</p><p>Y se mudó.</p><p>Y aquí la tenemos. Parte fundamental de la familia Caribbean Guard,.</p>",
  },
  {
    name: "Andrés “Tapas” Hernández",
    role: "Jefe de Búsqueda y Recuperación, Guardavidas y Pescador",
    photoFileId: "1YpQ5d_dtvr4nls8RGJR0xzXo2L2ztXg1",
    bioHtml:
      "<p><em>Jefe de Búsqueda y Recuperación Guardavidas/ Pescador</em><br><br>Nacido y criado en Punta Uva, es pescador de toda la vida, divemaster de buceo y “cazador” del pez león. Siempre consciente de su hábitat ha sido fundador de diferentes organizaciones como la “Asociación de Pescadores Artesanales del Caribe Sur”, la organización de buceo “Embajadores del Mar” y del reconocido “Gran Torneo de Pesca del Pez León”. Conoce el mar Caribe y sus playas como pocos, así también como sus ríos y creeks.</p><p>Cualquier búsqueda de víctimas o cuerpos que se haga en la provincia de Limón, ya sea en mar o rio, es altamente probable que “Tapas” esté involucrado.</p><p>Es una de las piezas fundamentales de la organización.</p>",
  },
  {
    name: "Melissa González",
    role: "Guardavidas e Instructora de Natación",
    photoFileId: "1T_8qT3CcWVOw8ysfLiMcLT-YeCycFzso",
    bioHtml:
      "<p><em>Guardavidas</em></p><p><em>Instructora de Natación</em></p><p>Es ateniense con orígenes puriscaleños y vive desde 2008 años en Talamanca, donde es docente de Educación Física en el Colegio de Paraíso, en Sixaola. Ha participado en simposios, congresos y llevado cursos técnicos para mantenerse actualizada en el ámbito del rendimiento deportivo y la natación.</p><p>Desde pequeña visitaba a su abuelita, que vivía frente al mar, en el Pacífico. En aquella época, soñaba con ser Guardavidas.</p><p><em>“Ahora tengo al Caribe frente a mí y Caribbean Guard hizo mi sueño realidad. Hoy sé la responsabilidad que tengo en prevenir y ayudar a las personas que visitan nuestra costa”.</em></p>",
  },
  {
    name: "Dexter Lewis",
    role: "Vicepresidente",
    photoFileId: "1PZ2hUrpQSajVE4wWhmeyrtLS1lFc0w1a",
    bioHtml:
      "<p><em>Línea fundadora</em></p><p><em>Guía de turismo/ Pro Surf</em></p><p>Nacido y criado en Puerto Viejo, empezó a surfear a los 13 años cuando el deporte se estaba popularizando en el Caribe. Una vez que corrió su primera ola, supo que su vida nunca volvería a ser la misma.</p><p>El surfing lo llevó a olas internacionales y diferentes brakes dentro del país, donde compitió profesionalmente y aprendió a surfear una gran variedad de olas.</p><p>¿La mejor ola que surfeó? “Está aquí en Puerto Viejo: Salsa Brava es una de las olas más icónicas y desafiantes de Centroamérica, y me inspira y desafía cada vez que voy afuera“.</p><p>Es instructor de surf, guía de turismo en el Caribe Sur y uno de los surfistas con más rescates acuáticos.</p><p><em>“Dediqué mi vida a enseñar en un ambiente seguro, donde hago énfasis en las técnicas para navegar las olas mientras ayudo a la gente a conectarse con el mar. Por esa misma vocación estoy en Caribbean Guard.”</em></p>",
  },
  {
    name: "Naima Montejo",
    role: "Instructora de Surf y Guardavidas",
    photoFileId: "1Esjp6pKaKT6NvBi-H7veKHtoN_KPAcud",
    bioHtml:
      "<p><em>Instructora de surf.</em></p><p><em>Guardavidas</em></p><p>Nacida en San José, su padre fue de la primera generación de surfistas de Costa Rica. Fue nadadora competitiva desde los 5 años hasta los 16, después empezó a hacer bodysurf —solo con el cuerpo— y a nadar en aguas abiertas. Enseguida experimentó con kayaks en olas y los 18 años empezó a surfear. A los 20 años comenzó a competir en el Circuito Nacional de Surf, en el cual participó por 3 años y luego se educó para ser guía e instructora de surf, a lo cual se dedica desde 2006, fundando su propia academia Surf Meds Caribe.</p><p>Crecida en el área de Punta Uva desde los 10 años, es una de las rescatistas más exitosas del Caribe Sur, como otros surfistas, por encontrarse casi a diario en su oficina: el mar, y por su sólida educación y experiencia acuática.</p>",
  },
  {
    name: "Joel Gaggstatter",
    role: "Fundador y Dron Unit",
    photoFileId: "1wF6ym34HGbsi1QDlBiSyoOUV6aHFW6sn",
    bioHtml:
      "<p><em>Fundador</em></p><p><em>Dron Unit</em></p><p>Creció en la zona de Puerto Viejo, siempre ha estado conectado con el mar; ya sea pescando, buceando o surfeando. Es una gran parte de su vida.&nbsp;</p><p>Es uno de los fundadores de BlueYouth, marca de ropa local inspirada en el mar y su cultura.&nbsp;</p><p>También está involucrado con la Asociación Coral Conservation, donde tienen la tarea de preservar los arrecifes coralinos del Caribe Sur.</p><p>Su idea de ayudar a crear y ser parte de Caribbean Guard nació por la importancia que sintió de prevenir y reducir la cantidad de ahogamientos en nuestras playas del Caribe Sur.</p>",
  },
  {
    name: "Gloriana Barrantes",
    role: "Guardavidas e Instructora de Natación",
    photoFileId: "1dKcojFJo6cyqwi9e9I38k8KJxoYv6t4c",
    bioHtml:
      "<p><em>Guardavidas</em></p><p><em>Instructora de natación.</em></p><p>Nacida en San Ramón de Alajuela, vive en Hone Creek desde 2017. Cuenta su mamá que aprendió a nadar antes que a caminar. Desde ahí nació su amor por el agua y el mar, que la llevó a aprender a bucear, a nadar en aguas abiertas, a conocer sobre corales, peces y sobre corrientes marinas.</p><p>Con Caribbean Guard se certificó como Guardavidas e Instructora de natación, actualmente colabora dando clases de natación a niños y adultos de la comunidad; también patrullando con el Club de Guardavidas.</p><p><em>“Hay que transmitir a los demás lo aprendido y así nos transformaremos en una comunidad más consciente en nuestra relación con el mar”.</em></p>",
  },
  {
    name: "Hershell Lewis",
    role: "Instructor de Surf y Guardavidas",
    photoFileId: "1XQZD8GuR-f82V4oS-sXhFSDNwP0dKSnS",
    bioHtml:
      "<p><em>Instructor de Surf<br>Guardavidas</em></p><p>Nacido y criado en Puerto Viejo, su relación con el mar es simbiótica: su abuelo y su padre fueron pescadores de la zona, empezó a surfear a los 10 años; es instructor de surf y S.U.P, de su propia escuela: CaribbeanSurfschoolandShop, desde el 2004.</p><p>Es certificado por la Internacional Surfing Association en surf y es instructor de rescate acuático por Mar Chen.</p><p>Es, muy probablemente, la persona con mayor cantidad de rescates acuáticos del Caribe y se lo conoce siempre por su buena vibra. Le gusta colaborar con Caribbean Guard y con su pueblo, ayudando a que las personas que lleguen a la playa estén seguras y que puedan regresar a casa con sus familiares.</p><p><em>“Recordemos que estuvimos nadando en el vientre de nuestra madre, la cual nos da una profunda conexión con el agua desde antes de haber nacido”.</em></p>",
  },
  {
    name: "Sofia Graff",
    role: "Guardavidas",
    photoFileId: "1wSv8Chv3yRe_E3HHezeNW7NvOsNTl6g6",
    bioHtml:
      "<p><em>Guardavidas</em></p><p>Nació en Estados Unidos y creció dentro y alrededor del agua. Fue nadadora competitiva en la escuela y pasó 6 años como guardavidas e instructora de natación para la Cruz Roja en los Estados Unidos.</p><p>Realizó el segundo curso de Guardavidas con Caribbean Guard y desde ahí se ha vuelto un elemento fundamental del grupo: ya sea dirigiendo entrenamientos de salvamento, en la parte educativa y patrullando.</p><p>Ama, con su esposo, estar horas en el mar haciendo snorkel y acaban de agrandar la familia con la preciosa Julia.</p><p>“Espero asegurarme de que todas las playas del Caribe sean seguras para que la gente disfrute de las bellezas del océano.”</p>",
  },
  {
    name: "AJ Smith",
    role: "Dron Unit",
    photoFileId: "1mgzzyLpCmswTOK61jlfTrhDHPAtrzaWK",
    bioHtml:
      "<p><em>Dron Unit</em></p><p>AJ creció en Texas y ha viajado extensivamente por el mundo. Desarrolló su pasión de toda la vida por estar dentro y alrededor del agua a una edad temprana y se convirtió en divemaster en la universidad. Desde surf y kayak hasta natación, apnea y pesca submarina, pasa la mayor parte posible del tiempo en el agua. Después de la trágica pérdida de un amigo durante un viaje de pesca submarina en alta mar, AJ comenzó a recibir capacitación en primeros auxilios para mejorar su capacidad y conciencia si alguna vez se encontraba nuevamente en esa posición. Ser parte de Caribbean Guard es una forma de utilizar sus habilidades y ayudar a hacer del área un lugar más seguro para las personas que viven y la visitan. Recientemente se mudó a Puerto Viejo con su familia y se siente afortunado de vivir en un lugar tan salvaje y hermoso. Él cree que la conexión con el océano es un regalo y le gustaría que todos tuvieran la oportunidad de experimentarlo.</p>",
  },
  {
    name: "Sofía Paso Viola",
    role: "Guardavidas, Guía de Turismo Aventura y Rescatista de Aguas Blancas",
    photoFileId: "1RvBLBt5PEGgTUVv8CXz8CIXtKwCXJLh2",
    bioHtml:
      "<p><em>Guardavidas</em></p><p><em>Guía de turismo Aventura/Rescatista de aguas blancas</em></p><p><em>Masajista</em></p><p>Nació en Mendoza, Argentina. Desde 2006 comenzó su carrera profesional y deportiva con el Rafting y Kayak. Siempre ha estado conectada con el río y la montaña.</p><p>Llegó a Costa Rica, en 2019 y se dedicó a la maternidad. Su hijo nació en Turrialba, y se mudaron a Puerto Viejo. Cuando cambió el rio por el mar, sintió la necesidad de conectarse con el agua y conoció Caribbean Guard. Desde hace un año es parte del programa y siente que es una&nbsp; forma de ayudar a la comunidad, ofrecer conocimientos y prevenir a las personas para que estén en el agua, disfrutando de un modo más seguro, con compañeros igual de apasionadxs por ponerse al servicio de la comunidad.</p>",
  },
  {
    name: "Melisa Gromöller",
    role: "Tesorera de la Junta Directiva",
    photoFileId: "1atBj9wFRsNcXyFlSucPlC_O7OiSH-ARk",
    bioHtml:
      "<p><em>Tesorera de la Junta Directiva</em></p><p>Nacida en Argentina, criada en Alemania y luego de viajar y trabajar por el mundo por más de 8 años finalmente, eligió el Caribe Sur de Costa Rica para vivir.</p><p>Tiene dos negocios gastronómicos en Puerto Viejo, ambos frente al mar. Es parte del equipo de natación en aguas abiertas de Playa Negra.&nbsp;</p><p><em>“Siempre pienso que el mar representa la libertad que la tierra no nos da y es la esencia del cambio constante. Aparenta ser una simple masa de agua donde el horizonte no parece tener fin, sin embargo esconde todo un universo de vida y de estados, siendo así la muestra empírica de que es posible crear un mundo donde quepan muchos mundos”.</em></p>",
  },
];

export const teamContent = {
  heading: '<h2 style="white-space:pre-wrap;">Familia de Mar</h2>',
  cardsTitle: "Conoce a nuestro equipo",
  cards: MEMBERS.map((m) => ({
    title: m.name,
    descriptionHtml: `<p>${m.role}</p>`,
    image: driveImage(m.photoFileId, m.name, 600),
  })),
  accordion: MEMBERS.map((m) => ({
    title: m.name,
    contentHtml: m.bioHtml,
  })),
};
