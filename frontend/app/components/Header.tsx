// app/components/Header.tsx
import { Button } from '../../components/ui/button';
import { Badge } from '../../components/ui/badge';
import { useSystemStore } from '../../lib/stores/system';

export const Header = () => {
    const { isRunning, network } = useSystemStore();

    return (
        <header className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
            <div className="container flex h-14 items-center">
                <div className="mr-4 hidden md:flex">
                    <a className="mr-6 flex items-center space-x-2" href="/">
                        <span className="hidden font-bold sm:inline-block">
                            🤖 QUANT AI DASHBOARD
                        </span>
                    </a>
                </div>
                <div className="flex flex-1 items-center justify-between space-x-2 md:justify-end">
                    <div className="w-full flex-1 md:w-auto md:flex-none">
                        {/* Search or other elements */}
                    </div>
                    <nav className="flex items-center space-x-2">
                        <Badge variant={isRunning ? 'default' : 'secondary'}>
                            {isRunning ? 'Running' : 'Stopped'}
                        </Badge>
                        <Badge variant="outline">{network}</Badge>
                    </nav>
                </div>
            </div>
        </header>
    );
};