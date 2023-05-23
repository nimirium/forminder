function deleteCookie(name: string): void {
    document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
}

export function hasSessionCookie(): boolean {
    return document.cookie.match(/^(.*;)?\s*session\s*=\s*[^;]+(.*)?$/) !== null;
}

export function logout() {
    deleteCookie('session');
    window.location.href = '/login';
}
