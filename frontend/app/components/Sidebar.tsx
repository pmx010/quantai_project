// app/components/Sidebar.tsx
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '../../lib/utils';
import { Button } from '../../components/ui/button';

const navigation = [
    { name: 'Dashboard', href: '/', icon: '📊' },
    { name: 'Trading', href: '/trades', icon: '💰' },
    { name: 'Agents', href: '/agents', icon: '🤖' },
    { name: 'Settings', href: '/settings', icon: '⚙️' },
    { name: 'Help', href: '/help', icon: '❓' },
];

export const Sidebar = () => {
    const pathname = usePathname();

    return (
        <div className="pb-12 w-64">
            <div className="space-y-4 py-4">
                <div className="px-3 py-2">
                    <h2 className="mb-2 px-4 text-lg font-semibold tracking-tight">
                        Navigation
                    </h2>
                    <div className="space-y-1">
                        {navigation.map((item) => (
                            <Button
                                key={item.name}
                                variant={pathname === item.href ? 'secondary' : 'ghost'}
                                className="w-full justify-start"
                                asChild
                            >
                                <Link href={item.href}>
                                    <span className="mr-2">{item.icon}</span>
                                    {item.name}
                                </Link>
                            </Button>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};