"use client";
import Link from "next/link"
import { usePathname } from "next/navigation";
import { ModeToggle } from "./mode-toggle";
import { cn } from "@/lib/utils";

export const Navigation = () => {
    const pathname = usePathname();
    
    const navItems = [
        { href: "/", label: "Home" },
        { href: "/about", label: "About" },
        { href: "/analytics", label: "Usage Stats" },
        { href: "/map", label: "Support Map" },
    ];

    return (
        <div className="flex h-14 items-center justify-between">
            <div className="flex items-center gap-6 md:gap-10">
                <Link href="/" className="font-semibold text-lg">
                    iAssist
                </Link>
                <nav className="flex gap-6">
                    {navItems.map((item) => (
                        <Link
                            key={item.href}
                            href={item.href}
                            className={cn(
                                "transition-colors hover:text-foreground/80",
                                pathname === item.href
                                    ? "text-foreground font-medium"
                                    : "text-foreground/60"
                            )}
                        >
                            {item.label}
                        </Link>
                    ))}
                </nav>
            </div>
            <div className="flex items-center gap-4">
                <ModeToggle />
            </div>
        </div>
    );
}