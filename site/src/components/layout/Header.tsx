"use client";

import Image from "next/image";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";

const NAV_LINKS = [
  { label: "Lifesaving Club", href: "/lifesaving-club" },
  { label: "Swim Club", href: "/swim-club" },
  { label: "Freediving Club", href: "/freediving-club" },
  { label: "Programa Playa Organizada", href: "/programa-playa-organizada" },
  { label: "Proyectos", href: "/proyectos" },
  { label: "Historia", href: "/nuestro-trabajo" },
  { label: "Team", href: "/team" },
  { label: "Involúcrate", href: "/involcrate" },
  { label: "Vision", href: "/vision" },
];

const LOGO_SRC =
  "https://lh3.googleusercontent.com/d/15ELvD6Khd76nPr-bkXtvlmaM8_k9qw_8=w400";

export default function Header() {
  const pathname = usePathname();
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    setMenuOpen(false);
  }, [pathname]);

  useEffect(() => {
    document.body.style.overflow = menuOpen ? "hidden" : "";
    return () => {
      document.body.style.overflow = "";
    };
  }, [menuOpen]);

  return (
    <header className="theme-white sticky top-0 z-50 border-b border-black/5 bg-background">
      <div className="mx-auto flex h-20 max-w-7xl items-center justify-between gap-6 px-6">
        <Link
          href="/"
          className="relative block h-10 w-36 shrink-0 md:h-14 md:w-44"
        >
          <Image
            src={LOGO_SRC}
            alt="Caribbean Guard"
            fill
            unoptimized
            priority
            referrerPolicy="no-referrer"
            className="object-contain object-left"
          />
        </Link>

        <nav
          className="hidden items-center gap-6 xl:flex"
          aria-label="Principal"
        >
          {NAV_LINKS.map((link) => {
            const active = pathname === link.href;
            return (
              <Link
                key={link.href}
                href={link.href}
                aria-current={active ? "page" : undefined}
                className={`text-sm font-medium whitespace-nowrap transition-colors hover:text-accent ${
                  active ? "text-accent" : "text-foreground"
                }`}
              >
                {link.label}
              </Link>
            );
          })}
        </nav>

        <div className="hidden xl:block">
          <Link
            href="/donar"
            className="rounded-md border-2 border-accent px-5 py-2 text-sm font-semibold whitespace-nowrap text-accent transition-colors hover:bg-accent hover:text-white"
          >
            Donar ahora
          </Link>
        </div>

        <button
          type="button"
          className="flex h-10 w-10 flex-col items-center justify-center gap-1.5 xl:hidden"
          aria-label={menuOpen ? "Cerrar menú" : "Abrir menú"}
          aria-expanded={menuOpen}
          onClick={() => setMenuOpen((open) => !open)}
        >
          <span
            className={`h-0.5 w-6 bg-foreground transition-transform ${
              menuOpen ? "translate-y-2 rotate-45" : ""
            }`}
          />
          <span
            className={`h-0.5 w-6 bg-foreground transition-opacity ${
              menuOpen ? "opacity-0" : "opacity-100"
            }`}
          />
          <span
            className={`h-0.5 w-6 bg-foreground transition-transform ${
              menuOpen ? "-translate-y-2 -rotate-45" : ""
            }`}
          />
        </button>
      </div>

      {menuOpen && (
        <div className="fixed inset-x-0 top-20 bottom-0 z-40 flex flex-col bg-background xl:hidden">
          <nav
            className="flex flex-1 flex-col gap-1 overflow-y-auto px-6 py-8"
            aria-label="Principal móvil"
          >
            {NAV_LINKS.map((link) => {
              const active = pathname === link.href;
              return (
                <Link
                  key={link.href}
                  href={link.href}
                  aria-current={active ? "page" : undefined}
                  className={`border-b border-black/5 py-4 text-lg font-medium ${
                    active ? "text-accent" : "text-foreground"
                  }`}
                >
                  {link.label}
                </Link>
              );
            })}
          </nav>
          <div className="shrink-0 border-t border-black/5 px-6 py-4">
            <Link
              href="/donar"
              className="block rounded-md bg-accent px-5 py-3 text-center text-base font-semibold text-white"
            >
              Donar ahora
            </Link>
          </div>
        </div>
      )}
    </header>
  );
}
