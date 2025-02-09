"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { ModeToggle } from "./mode-toggle";
import Image from "next/image";
import { useTheme } from "next-themes";
import { cn } from "@/lib/utils";
import { useEffect, useState } from "react";
import { AnimatedText } from "@/components/ui/animated-underline-text-one";

export const Navigation = () => {
    const pathname = usePathname();
    const { theme } = useTheme();
    const [mounted, setMounted] = useState(false);

    useEffect(() => {
        setMounted(true);
    }, []);

    const navItems = [
        { href: "/", label: "Home" },
        { href: "/about", label: "About" },
        { href: "/why", label: "Why" },
    ];

    return (
        <nav className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
            <div className="max-w-screen-xl mx-auto px-4">
                <div className="flex h-20 items-center justify-between">
                    <div className="flex items-center gap-8">
                        <Link href="/" className="flex items-center gap-2">
                            {mounted && (
                                <Image
                                    src={theme === 'dark' ? '/logo/logo_dark.png' : '/logo/logo_dark.png'}
                                    alt="iAssist Logo"
                                    width={80}
                                    height={80}
                                    className="w-40 h-40"
                                    priority
                                />
                            )}
                        </Link>
                        
                        <div className="hidden md:flex md:gap-10">
                            {navItems.map((item) => (
                                <Link
                                    key={item.href}
                                    href={item.href}
                                    className={cn(
                                        "text-lg font-semibold transition-colors hover:text-primary",
                                        pathname === item.href
                                            ? "text-foreground"
                                            : "text-foreground/60"
                                    )}
                                >
                                    {item.label}
                                </Link>
                            ))}
                        </div>
                    </div>

                    <div className="flex items-center gap-4">
                        <ModeToggle />
                    </div>
                </div>
            </div>
        </nav>
    );
}