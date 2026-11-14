import type { Register, ThemeSetArgs } from 'claude-code'

import { makeColors } from './make-colors.js'
import { SCENE } from './scene'

// Rosé Pine (main), from github.com/rose-pine/palette, dark only by request.
const { theme, problems } = makeColors({
  label: 'ocsky galaxy',
  only: 'dark',
  roles: { accent: '#c4a7e7', danger: '#eb6f92', success: '#9ccfd8', warning: '#f6c177', pro: '#ebbcba' },
  dark: {
    gray: {
      anchors: {
        'surface-0': '#191724',
        'surface-1': '#1f1d2e',
        'surface-2': '#26233a',
        'surface-3': '#26233a',
        'text-primary': '#e0def4',
        'text-secondary': '#c8c5e0',
        'text-muted': '#908caa',
      },
    },
  },
})

const LOOK: ThemeSetArgs = { colors: theme, backdrop: { scene: 'galaxy', glass: false } }

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    const unpainted = problems.find(line => line.startsWith("Desktop won't paint"))
    if (unpainted !== undefined) {
      $.ui.toast(unpainted)
    }
    const set = await $.theme.set(LOOK)
    if (!set.isDrawn) {
      $.ui.status(set.reason)
    }
    return next(e)
  })

  // A spiral of square grains on a grid, after ocsky's braille galaxy, turning once every four minutes.
  on('ui.render', { component: 'Backdrop' }, ($, e, next) => {
    if (e.surface !== 'desktop' && e.surface !== 'mobile') {
      return next(e)
    }
    const { Svg } = $.ui.resolve(e)
    return <Svg source={SCENE} alt="A dotted spiral galaxy turning slowly among faint stars" />
  })
}
