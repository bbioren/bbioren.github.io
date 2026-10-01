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
        },{id: "post-the-convex-conjugate-is-a-list-of-supporting-lines",
      
        title: "the convex conjugate is a list of supporting lines",
      
      description: "for each slope, how far down do you have to push a line so it supports the graph?",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2026/convex-conjugate-supporting-lines/";
        
      },
    },{id: "post-linearity-of-expectation-needs-nothing",
      
        title: "linearity of expectation needs nothing",
      
      description: "why adding expectations never requires independence, and how indicator variables turn hard counting into bookkeeping",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2026/linearity-of-expectation-needs-nothing/";
        
      },
    },{id: "post-which-way-does-kl-point",
      
        title: "which way does kl point?",
      
      description: "forward kl covers every mode, reverse kl picks one, and the two most common objectives in machine learning point in opposite directions",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2026/which-way-kl/";
        
      },
    },{id: "post-where-the-root-pi-comes-from",
      
        title: "where the root pi comes from",
      
      description: "the gaussian integral, and the circle hiding inside every bell curve",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2026/where-the-root-pi-comes-from/";
        
      },
    },{id: "post-bayes-39-theorem-in-a-square",
      
        title: "bayes&#39; theorem in a square",
      
      description: "conditioning is zooming in, and the base rate decides what you see when you get there",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2026/bayes-theorem-in-a-square/";
        
      },
    },{id: "post-why-n-minus-one",
      
        title: "why n minus one",
      
      description: "the degree of freedom you lose to the sample mean is literally a dimension",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2026/why-n-minus-one/";
        
      },
    },{id: "post-cauchy-schwarz-is-a-shadow",
      
        title: "cauchy–schwarz is a shadow",
      
      description: "why a projection is never longer than the vector it came from",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2026/cauchy-schwarz-shadows/";
        
      },
    },{id: "post-lagrange-multipliers-are-a-tangency-condition",
      
        title: "lagrange multipliers are a tangency condition",
      
      description: "why the gradients line up at a constrained optimum, and what the multiplier is actually measuring",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2026/lagrange-multipliers-tangency/";
        
      },
    },{id: "post-why-the-gradient-points-uphill",
      
        title: "why the gradient points uphill",
      
      description: "the vector of partials is the steepest direction because, up close, every function is a plane",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2026/why-the-gradient-points-uphill/";
        
      },
    },{id: "post-jensen-39-s-inequality-is-a-picture",
      
        title: "jensen&#39;s inequality is a picture",
      
      description: "chords lie above convex curves, and that is the whole inequality",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2026/jensens-inequality/";
        
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
            },},{id: "projects-appmixer",
          title: 'AppMixer',
          description: "Per-app volume mixer for macOS using CoreAudio taps",
          section: "Projects",handler: () => {
              window.location.href = "/projects/app_mixer/";
            },},{id: "projects-area-of-a-circle",
          title: 'Area of a Circle',
          description: "Visual intuition for the area of a circle!",
          section: "Projects",handler: () => {
              window.location.href = "/projects/circ_area/";
            },},{id: "projects-gradescope-extension",
          title: 'Gradescope Extension',
          description: "Chrome extension for viewing grade statistics on Gradescope",
          section: "Projects",handler: () => {
              window.location.href = "/projects/gradescope_extension/";
            },},{id: "projects-patch-39-n-play",
          title: 'Patch &amp;#39;n Play',
          description: "Community soccer net repair project",
          section: "Projects",handler: () => {
              window.location.href = "/projects/patch_n_play/";
            },},{id: "projects-speedup-extension",
          title: 'Speedup Extension',
          description: "Chrome extension to control playback speed on any website",
          section: "Projects",handler: () => {
              window.location.href = "/projects/speedup_extension/";
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
