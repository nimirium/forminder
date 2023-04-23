function removeURLParameter(url: string, parameter: string): string {
    const urlparts = url.split('?');
    if (urlparts.length >= 2) {

        const prefix = encodeURIComponent(parameter) + '=';
        const pars = urlparts[1].split(/[&;]/g);

        for (let i = pars.length; i-- > 0;) {
            if (pars[i].lastIndexOf(prefix, 0) !== -1) {
                pars.splice(i, 1);
            }
        }

        return urlparts[0] + (pars.length > 0 ? '?' + pars.join('&') : '');
    }
    return url;
}


export function removeCodeUrlParameter() {
    if (window.history.pushState) {
        let newUrl = removeURLParameter(window.location.href, 'code');
        newUrl = removeURLParameter(newUrl, 'state');
        window.history.pushState({}, '', newUrl);
    }
}
