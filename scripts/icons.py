"""Small inline icons for navigation and social links; labels belong to the link."""
ICONS = {
 'brand': '<rect x="3" y="3" width="7" height="7" rx="1" fill="currentColor"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>',
 'home': '<path d="M12 5c-3-2-6-2-9-1v15c3-1 6-1 9 1 3-2 6-2 9-1V4c-3-1-6-1-9 1Zm0 0v15"/>',
 'projects': '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>',
 'experience': '<rect x="3" y="7" width="18" height="14" rx="2"/><path d="M8 7V3h8v4M3 12c5 3 13 3 18 0M12 12v4"/>',
 'about': '<circle cx="12" cy="7" r="4"/><path d="M4 21v-2a8 8 0 0 1 16 0v2"/>',
 'recognition': '<circle cx="12" cy="9" r="6"/><path d="m8 14-2 7 6-3 6 3-2-7"/>',
 'contact': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 6 9 7 9-7"/>',
 'linkedin': '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M7 10v7m5 0v-7m0 3a3 3 0 0 1 6 0v4"/><circle cx="7" cy="7" r=".7" fill="currentColor"/>',
 'github': '<path d="M9 20c-5 1-5-2-7-2m14 4v-4c0-1-.3-2-1-2.5 3-.4 6-1.5 6-6a5 5 0 0 0-1.5-3.5c.1-1 .1-2-.5-3-2 0-3.5 1-4 1.5a13 13 0 0 0-6 0C8 4 6.5 3 5 3c-.6 1-.6 2-.5 3A5 5 0 0 0 3 9.5c0 4.5 3 5.6 6 6-.7.5-1 1.5-1 2.5v4"/>',
 'top': '<path d="M5 6h14M6 14l6-6 6 6M12 8v13"/>',
 'previous': '<path d="m14 5-7 7 7 7"/>',
 'next': '<path d="m10 5 7 7-7 7"/>',
 'zoom': '<path d="M4 9V4h5m6 0h5v5M4 15v5h5m6 0h5v-5"/>',
}
def icon(name):
 return f'<svg class="ui-icon icon-{name}" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{ICONS[name]}</svg>'
