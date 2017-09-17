import React, { Component } from 'react'

import { BarChart, LineChart } from 'react-d3-basic'

const chartSeries = [{
  field: 'val',
  name: 'Value',
}]
const colorSeries = [{
  field: 'val',
  name: 'Value',
  color: '#24C0D9'
}]
const HEIGHT = 900
const WIDTH = 1600

const x = e => e.i
const M = 676171
const N = 100

function* gen1 () {
  let seed = 1994
  while (true) {
    let sqr = seed ** 2
    let str = String(sqr)
    if (str.length < 8) {
      for (let i = 0; i < 8 - str.length; i++) {
        str = '0' + str
      }
    }
    seed = parseInt(str.slice(2, 6), 10)
    yield seed
  }
}

function* gen2 () {
  let A = 1994
  const k = 271129
  while (true) {
    A = (A * k) % M
    yield A
  }
}

class App extends Component {

  constructor(props) {
    super(props)
    const g1 = gen1()
    const g2 = gen2()
    const a1 = []
    const a2 = []
    const p1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    const p2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for (let i = 1; i <= N; i++) {
      const t1 = g1.next().value
      const t2 = g2.next().value
      a1.push({ i, val: t1 })
      a2.push({ i, val: t2 })
      let i1 = Math.round(t1 / 1000)
      i1 = i1 === 10 ? 0 : i1
      p1[i1] = p1[i1] + 1
      let i2 = Math.round(t2 / M * 10)
      i2 = i2 === 10 ? 0 : i2
      p2[i2] = p2[i2] + 1
    }

    this.state = {
      a1,
      a2,
      p1: p1.map((x, i) => ({ i: i + 1, val: x / N })),
      p2: p2.map((x, i) => ({ i: i + 1, val: x / N })),
    }
    console.log(p1)
  }

  render () {
    const { a1, a2, p1, p2 } = this.state
    console.log(p1)
    console.log(p2)
    return (
      <div>
        <BarChart
          data={a1}
          width={WIDTH}
          height={HEIGHT}
          chartSeries={chartSeries}
          x={x}
          xScale='ordinal'
        />
        <BarChart
          data={a2}
          width={WIDTH}
          height={HEIGHT}
          chartSeries={chartSeries}
          x={x}
          xScale='ordinal'
        />
        <LineChart
          data={p1}
          width={WIDTH}
          height={HEIGHT}
          chartSeries={colorSeries}
          x={x}
          xScale='ordinal'
        />
        <LineChart
          data={p2}
          width={WIDTH}
          height={HEIGHT}
          chartSeries={colorSeries}
          x={x}
          xScale='ordinal'
        />
      </div>
    )
  }
}

export default App
