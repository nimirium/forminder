export let apiURL: string;

if (import.meta.env.VITE_ENV === 'development') {
    apiURL = 'http://localhost:5000';  // your Flask server's development URL
} else if (import.meta.env.VITE_ENV === 'production') {
    apiURL = import.meta.env.VITE_DOMAIN;  // your Flask server's production URL
}
