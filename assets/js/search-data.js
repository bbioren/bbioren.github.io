// get the ninja-keys element
const ninja = document.querySelector('ninja-keys');

// add the home and posts menu items
ninja.data = [{
    id: "nav-about",
    title: "about",
    section: "Navigation",
    handler: () => {
      window.location.href = "/";
    },
  },{id: "nav-blog",
          title: "blog",
          description: "",
          section: "Navigation",
          handler: () => {
            window.location.href = "/blog/";
          },
        },{id: "nav-projects",
          title: "projects",
          description: "Some projects I have worked on.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/projects/";
          },
        },{id: "post-the-bicycle",
      
        title: "the bicycle",
      
      description: "a motif turned philosophy",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2025/theBicycle/";
        
      },
    },{id: "projects-crispr-apples",
          title: 'CRISPR Apples',
          description: "Dubhacks 25 Winner",
          section: "Projects",handler: () => {
              window.location.href = "/projects/CRISPR_apples/";
            },},{id: "projects-area-of-a-circle",
          title: 'Area of a Circle',
          description: "Visual intuition for the area of a circle!",
          section: "Projects",handler: () => {
              window.location.href = "/projects/circ_area/";
            },},{id: "projects-patch-39-n-play",
          title: 'Patch &amp;#39;n Play',
          description: "Community soccer net repair project",
          section: "Projects",handler: () => {
              window.location.href = "/projects/patch_n_play/";
            },},{
        id: 'social-email',
        title: 'email',
        section: 'Socials',
        handler: () => {
          window.open("mailto:%62%62%69%6F%72%65%6E@%75%77.%65%64%75", "_blank");
        },
      },{
        id: 'social-github',
        title: 'GitHub',
        section: 'Socials',
        handler: () => {
          window.open("https://github.com/bbioren", "_blank");
        },
      },{
        id: 'social-linkedin',
        title: 'LinkedIn',
        section: 'Socials',
        handler: () => {
          window.open("https://www.linkedin.com/in/ben-bioren", "_blank");
        },
      },{
        id: 'social-rss',
        title: 'RSS Feed',
        section: 'Socials',
        handler: () => {
          window.open("/feed.xml", "_blank");
        },
      },{
      id: 'light-theme',
      title: 'Change theme to light',
      description: 'Change the theme of the site to Light',
      section: 'Theme',
      handler: () => {
        setThemeSetting("light");
      },
    },
    {
      id: 'dark-theme',
      title: 'Change theme to dark',
      description: 'Change the theme of the site to Dark',
      section: 'Theme',
      handler: () => {
        setThemeSetting("dark");
      },
    },
    {
      id: 'system-theme',
      title: 'Use system default theme',
      description: 'Change the theme of the site to System Default',
      section: 'Theme',
      handler: () => {
        setThemeSetting("system");
      },
    },];
