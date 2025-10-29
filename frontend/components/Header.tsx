'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function Header() {
  const pathname = usePathname();

  const navLinks = [
    { href: '/', label: 'Dashboard' },
    { href: '/marketing', label: 'Marketing Materials' },
  ];

  return (
    <header className="bg-red-700 text-white shadow-md">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo/Title */}
          <div className="flex items-center">
            <h1 className="text-xl font-bold">LaPorte FC</h1>
          </div>

          {/* Navigation */}
          <nav>
            <ul className="flex space-x-6">
              {navLinks.map((link) => (
                <li key={link.href}>
                  <Link
                    href={link.href}
                    className={`hover:text-gray-200 transition-colors px-3 py-2 rounded ${
                      pathname === link.href
                        ? 'bg-red-800 font-semibold'
                        : ''
                    }`}
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </nav>
        </div>
      </div>
    </header>
  );
}
