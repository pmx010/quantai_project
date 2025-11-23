// lib/formatters.ts
import { format, formatDistanceToNow } from 'date-fns';

export const formatCurrency = (value: number): string => {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 2,
        maximumFractionDigits: 4,
    }).format(value);
};

export const formatPercentage = (value: number): string => {
    return `${(value * 100).toFixed(2)}%`;
};

export const formatNumber = (value: number, decimals: number = 2): string => {
    return value.toFixed(decimals);
};

export const formatDate = (date: string | Date): string => {
    return format(new Date(date), 'MMM dd, yyyy HH:mm:ss');
};

export const formatRelativeTime = (date: string | Date): string => {
    return formatDistanceToNow(new Date(date), { addSuffix: true });
};

export const formatTokenAmount = (amount: number, token: string): string => {
    return `${formatNumber(amount)} ${token}`;
};