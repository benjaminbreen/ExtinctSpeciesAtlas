// Original, deliberately small woodcut-style details for the colored seal.
// Dark shapes act as printed ink; accent-colored strokes are carved highlights.
// They are interface drawings, not copies of historical species illustrations.
export const sealMarks = {
  silphium: `
    <path d="M50 15c-6 8-12 12-16 24-4 13-4 28 1 39 3 7 8 12 15 15 7-3 12-8 15-15 5-11 5-26 1-39-4-12-10-16-16-24Z" fill="currentColor" fill-opacity=".23" stroke-width="1.7"/>
    <path d="M50 20c-8 8-12 20-14 35-1 14 4 25 14 34-6-14-8-29-7-42 1-11 3-19 7-27Zm0 0c8 8 12 20 14 35 1 14-4 25-14 34 6-14 8-29 7-42-1-11-3-19-7-27Z" fill="currentColor" fill-opacity=".23" stroke="none"/>
    <path d="M50 6v14m-3-11 3-4 3 4M50 91v5" stroke-width="1.9"/>
    <g fill="none" stroke-linecap="round">
      <path d="M50 22c-6 12-9 24-9 36 0 14 3 23 9 31m0-67c6 12 9 24 9 36 0 14-3 23-9 31" stroke-width="1.8"/>
      <path d="M42 29c-4 12-5 28-3 42m19-42c4 12 5 28 3 42M50 25v60" stroke-width="1.15"/>
      <path d="m36 43 4 2m-5 8 5 2m-5 8 5 2m-3 8 5 2m22-32-4 2m5 8-5 2m5 8-5 2m-3 8-5 2" stroke-width=".9" opacity=".55"/>
    </g>
  `,
  auk: `
    <path d="M18 84c0-14 2-29 8-40 6-12 16-19 28-19 12 0 17 6 20 11l17 3-12 10-13 2c-6 4-10 11-11 18l-1 17Z" fill="currentColor" stroke-width="1.2"/>
    <path d="M74 36c-4 3-9 7-15 10l19 2m-24 21c-3 3-6 8-7 15" stroke-width="1.4"/>
    <g stroke="var(--accent)" fill="none"><path d="M26 76c0-20 8-38 22-43m-16 48c-1-16 3-28 11-37m-4 36c-1-10 1-18 5-24" stroke-width="1.7"/>
      <path d="m64 39 12 2m-13 3 9 2m-14 3 10 1" stroke-width="1.5"/>
      <circle cx="56" cy="36" r="2.8" fill="var(--accent)" stroke="none"/></g>
    <circle cx="56" cy="36" r="1" fill="currentColor" stroke="none"/>
  `,
  seacow: `
    <path d="M50 54C36 41 20 49 6 29c3 19 9 31 21 37 7 4 15 4 23 0 8 4 16 4 23 0 12-6 18-18 21-37-14 20-30 12-44 25Z" fill="currentColor" stroke-width="1.2"/>
    <path d="M50 66c-1 8-1 17 0 25" stroke-width="2"/>
    <g stroke="var(--accent)" fill="none" stroke-width="1.9">
      <path d="M12 39c8 14 20 20 35 20m-29-13c7 9 16 13 27 13m-22-8c6 5 12 7 18 7M88 39c-8 14-20 20-35 20m29-13c-7 9-16 13-27 13m22-8c-6 5-12 7-18 7"/>
    </g>
  `,
  dodo: `
    <path d="M20 83c-3-19 1-40 12-51 8-9 19-11 29-7 9 4 14 12 14 22l15 1c-2 10-9 18-20 21-7 2-14-1-19-4-5 7-8 14-8 20Z" fill="currentColor" stroke-width="1.2"/>
    <path d="M75 47c-2 9-7 15-14 18 13 1 23-5 28-16M33 85c0-12 2-23 8-33" stroke-width="1.4"/>
    <g stroke="var(--accent)" fill="none">
      <path d="M28 74c1-15 5-30 15-38m-9 43c1-13 5-24 12-31m-8 35c1-9 3-17 8-24" stroke-width="1.7"/>
      <path d="M63 50c3 5 5 7 10 8m4-3 6-3" stroke-width="2"/>
      <circle cx="58" cy="39" r="3" fill="var(--accent)" stroke="none"/>
    </g>
    <circle cx="59" cy="39" r="1" fill="currentColor" stroke="none"/>
  `,
  aurochs: `
    <path d="M35 42C19 41 9 29 12 10c3 12 10 18 20 20l9 4-6 8Zm30 0c16-1 26-13 23-32-3 12-10 18-20 20l-9 4 6 8Z" fill="currentColor" stroke-width="1.3"/>
    <path d="M36 38c-2 9-1 17 4 23l10 4 10-4c5-6 6-14 4-23-7-6-21-6-28 0Z" fill="currentColor" stroke-width="1.3"/>
    <path d="M41 61c0 8 4 17 9 27 5-10 9-19 9-27" fill="currentColor" stroke-width="1.3"/>
    <g stroke="var(--accent)" fill="none"><path d="M16 19c5 11 12 16 22 17m46-17c-5 11-12 16-22 17M39 42c2 5 5 8 11 10 6-2 9-5 11-10M43 62c1 7 3 13 7 20m7-20c-1 7-3 13-7 20" stroke-width="1.8"/>
      <path d="M41 38c5-3 13-3 18 0" stroke-width="1.1"/></g>
  `,
  solitaire: `
    <path d="M19 88c2-23 12-39 27-43l3-20c2-11 10-17 19-15 7 2 10 8 10 15l12 4-9 9-12 2c-5 7-8 14-8 22l2 27Z" fill="currentColor" stroke-width="1.2"/>
    <path d="M78 25c-1 6-4 10-9 15m-22 5c5 7 8 15 8 23" stroke-width="1.4"/>
    <g stroke="var(--accent)" fill="none"><path d="M29 82c2-15 8-24 18-29m-11 31c1-11 5-19 12-24m-6 25c1-7 3-13 7-17M54 25c2-6 6-10 11-11" stroke-width="1.7"/>
      <circle cx="67" cy="24" r="2.6" fill="var(--accent)" stroke="none"/></g>
    <circle cx="67" cy="24" r=".9" fill="currentColor" stroke="none"/>
  `,
  saddle: `
    <path d="M14 75c3-23 14-42 31-48 13-4 24 2 30 18l4-13 10-7 7 10-12 5-5 25-11 14H25Z" fill="currentColor" stroke-width="1.2"/>
    <path d="M17 76h54m8-31 8-10" stroke-width="1.4"/>
    <g stroke="var(--accent)" fill="none"><path d="M24 61c16-4 30-2 48 7M34 37c5 10 6 23 3 37m17-43c-4 13-4 26 0 43M20 68c15-1 32 1 45 6" stroke-width="1.9"/>
      <path d="m30 52 8 4m8-12 8 6m5 10 8 4" stroke-width="1.2"/></g>
  `,
  domed: `
    <path d="M10 77c1-29 17-49 40-49s39 20 40 49H10Z" fill="currentColor" stroke-width="1.3"/>
    <path d="M10 77h80" stroke-width="1.5"/>
    <g stroke="var(--accent)" fill="none"><path d="M50 30v45M31 38c-6 11-9 23-9 37m47-37c6 11 9 23 9 37M15 61c12-2 24 1 35 8 11-7 23-10 35-8M32 40c6 7 12 10 18 10s12-3 18-10" stroke-width="1.8"/>
      <path d="m20 66 6 3m48 0 6-3M38 52l5 4m14 0 5-4" stroke-width="1.1"/></g>
  `,
  bluebuck: `
    <path d="M39 49C26 39 19 23 27 7c-1 17 10 24 22 36l-10 6Zm22 0C74 39 81 23 73 7c1 17-10 24-22 36l10 6Z" fill="currentColor" stroke-width="1.2"/>
    <path d="M38 42c-5 10-6 20-2 28l14 19 14-19c4-8 3-18-2-28-7-7-17-7-24 0Z" fill="currentColor" stroke-width="1.2"/>
    <g stroke="var(--accent)" fill="none"><path d="M28 18c2 11 8 18 15 22m29-22c-2 11-8 18-15 22M40 48c2 7 6 13 10 17 4-4 8-10 10-17m-17 24 7 12 7-12" stroke-width="1.8"/>
      <path d="m32 26 5 4m-4-13 4 5m31 4-5 4m4-13-4 5" stroke-width="1.2"/></g>
  `,
  bluepigeon: `
    <path d="M48 9c14 13 23 26 23 42 0 17-9 29-22 40C36 79 27 65 27 50c0-16 8-29 21-41Z" fill="currentColor" stroke-width="1.2"/>
    <path d="M49 18v72" stroke="var(--accent)" stroke-width="2"/>
    <g stroke="var(--accent)" fill="none" stroke-width="1.8"><path d="M48 28 37 36m11 2-15 9m15 2-17 9m17 2-14 10m14 1-10 9m11-52 11 8m-11 2 15 9m-15 2 17 9m-17 2 14 10m-14 1 10 9"/></g>
    <path d="m29 45-7 6 7 5-5 5 7 5m39-21 7 6-7 5 5 5-7 5" stroke-width="1.4"/>
  `,
  macaw: `
    <path d="M18 81c-1-17 4-31 15-41 10-9 24-12 35-5 7 4 10 12 9 20l14 1c-3 12-13 22-29 23-9 1-16-2-20-9l-6 17Z" fill="currentColor" stroke-width="1.2"/>
    <path d="M77 54c-2 11-8 18-17 23 15 0 26-8 31-20" stroke-width="1.5"/>
    <g stroke="var(--accent)" fill="none"><path d="M25 76c1-13 7-23 16-30m-10 34c3-12 8-20 16-26m-9 29c3-9 7-16 13-21M43 38c4 4 6 9 7 15m-2-18c5 4 7 8 9 15m-2-17c5 4 7 9 8 14" stroke-width="1.8"/>
      <circle cx="65" cy="43" r="2.7" fill="var(--accent)" stroke="none"/></g>
    <circle cx="65" cy="43" r="1" fill="currentColor" stroke="none"/>
  `,
  warrah: `
    <path d="M15 82c4-16 13-29 28-35l-2-30 14 20 14-3 11-16 1 28c5 5 8 10 9 17l5 7-13 6-14-3-16 15Z" fill="currentColor" stroke-width="1.2"/>
    <path d="M43 47c5 7 10 13 12 23m22-13 13 7m-17 9 9 4" stroke-width="1.4"/>
    <g stroke="var(--accent)" fill="none"><path d="M24 75c6-12 14-19 24-23m-17 27c6-10 12-16 21-20m-13 22c5-7 10-13 15-16M45 27l5 12m26-9-9 13M70 52c3 4 5 9 6 13" stroke-width="1.8"/>
      <circle cx="77" cy="54" r="2.5" fill="var(--accent)" stroke="none"/></g>
    <circle cx="77" cy="54" r=".9" fill="currentColor" stroke="none"/>
  `
};
