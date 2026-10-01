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
  },{id: "post-markov-chebyshev-chernoff",
      
        title: "markov, chebyshev, chernoff",
      
      description: "three tail bounds, one trick, and how much each extra assumption buys you",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2026/markov-chebyshev-chernoff/";
        
      },
    },{id: "post-the-convex-conjugate-is-a-list-of-supporting-lines",
      
        title: "the convex conjugate is a list of supporting lines",
      
      description: "for each slope, how far down a line has to go before it fits under the graph",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2026/convex-conjugate-supporting-lines/";
        
      },
    },{id: "post-consistent-hashing",
      
        title: "consistent hashing",
      
      description: "why a hash ring moves far fewer keys than hash mod N when servers come and go.",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2026/consistent-hashing/";
        
      },
    },{id: "post-linearity-of-expectation-needs-nothing",
      
        title: "linearity of expectation needs nothing",
      
      description: "adding expectations doesn&#39;t need independence, shown with a table of returned hats",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2026/linearity-of-expectation-needs-nothing/";
        
      },
    },{id: "post-three-ways-to-shard",
      
        title: "three ways to shard",
      
      description: "data, tensor, and pipeline parallelism on 4 devices, animated.",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2026/three-ways-to-shard/";
        
      },
    },{id: "post-which-way-does-kl-point",
      
        title: "which way does kl point?",
      
      description: "fitting one gaussian to a two-bump distribution with forward and reverse kl gives two very different answers",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2026/which-way-kl/";
        
      },
    },{id: "post-flash-attention",
      
        title: "flash attention",
      
      description: "exact attention without ever storing the N by N score matrix",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2026/flash-attention/";
        
      },
    },{id: "post-where-the-root-pi-comes-from",
      
        title: "where the root pi comes from",
      
      description: "where the pi in the normal distribution comes from",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2026/where-the-root-pi-comes-from/";
        
      },
    },{id: "post-systolic-array",
      
        title: "systolic array",
      
      description: "how ML accelerators multiply matrices, one cycle at a time",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2026/systolic-array/";
        
      },
    },{id: "post-bayes-39-theorem-in-a-square",
      
        title: "bayes&#39; theorem in a square",
      
      description: "a positive test for a rare disease, drawn to scale",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2026/bayes-theorem-in-a-square/";
        
      },
    },{id: "post-tiled-matrix-multiply",
      
        title: "tiled matrix multiply",
      
      description: "why loading tiles into on-chip memory makes matmul fast",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2026/tiled-matmul/";
        
      },
    },{id: "post-why-n-minus-one",
      
        title: "why n minus one",
      
      description: "the lost degree of freedom is a direction you can draw",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2026/why-n-minus-one/";
        
      },
    },{id: "post-fourier-epicycles",
      
        title: "fourier epicycles",
      
      description: "spinning circles stacked end to end that trace any closed curve",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2026/fourier-epicycles/";
        
      },
    },{id: "post-cauchy-schwarz-is-a-shadow",
      
        title: "cauchy–schwarz is a shadow",
      
      description: "a projection is never longer than the vector it came from",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2026/cauchy-schwarz-shadows/";
        
      },
    },{id: "post-galton-board",
      
        title: "galton board",
      
      description: "a live galton board that grows a bell curve",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2026/galton-board/";
        
      },
    },{id: "post-lagrange-multipliers-are-a-tangency-condition",
      
        title: "lagrange multipliers are a tangency condition",
      
      description: "why the gradients line up at a constrained optimum, and what lambda means",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2026/lagrange-multipliers-tangency/";
        
      },
    },{id: "post-buffon-39-s-needle",
      
        title: "buffon&#39;s needle",
      
      description: "drop needles on lined paper and watch them count out pi",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2026/buffons-needle/";
        
      },
    },{id: "post-why-the-gradient-points-uphill",
      
        title: "why the gradient points uphill",
      
      description: "where the directional derivative formula comes from and what it says about steepest ascent",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2026/why-the-gradient-points-uphill/";
        
      },
    },{id: "post-pythagoras-by-rearrangement",
      
        title: "pythagoras by rearrangement",
      
      description: "slide four triangles around a square and watch a² + b² = c² fall out",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2026/pythagoras-rearrangement/";
        
      },
    },{id: "post-jensen-39-s-inequality-is-a-picture",
      
        title: "jensen&#39;s inequality is a picture",
      
      description: "why the average of a convex function sits above the function of the average",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2026/jensens-inequality/";
        
      },
    },{id: "post-area-of-a-circle",
      
        title: "area of a circle",
      
      description: "visual intuition for the area of a circle!",
      section: "Posts",
      handler: () => {
        
          window.location.href = "/blog/2025/area-of-a-circle/";
        
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
            },},{id: "projects-gradescope-extension",
          title: 'Gradescope Extension',
          description: "Chrome extension for viewing grade statistics on Gradescope",
          section: "Projects",handler: () => {
              window.location.href = "/projects/gradescope_extension/";
            },},{id: "projects-matchvision",
          title: 'MatchVision',
          description: "Berkeley AI Hackathon 2026 winner (Best Use of Terac). A voice-first soccer companion for blind and low-vision fans.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/match_vision/";
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
