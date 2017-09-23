import React, { Component } from 'react';
import * as V from 'victory';
import { VictoryChart, VictoryLine, VictoryAxis, VictoryTheme } from 'victory'
import {
  gen1,
  gen2,
  getK,
} from './lib'

class App extends Component {

  constructor(props) {
    super(props)
    const g1 = gen1()
    const g2 = gen2()
    const n = 100
    const k = getK(n)
    const a1 = []
    for (let i = 0; i < n; i++) {
      const v1 = g1.next().value
      const l = g2.next().value
      //a1.push({ x: i, y: v1, k: Math.ceil(v1 * k) })
      console.log(i, k, l)
    }
    this.state = {
      m: 676171,
      k,
      n,
      a1,
    }
  }

  componentDidMount() {
    this.update()
  }

  update = () => {
    const { m, n } =  this.state
    const g1 = gen1()
    const g2 = gen2()
    const k = getK(n)
    const k1 = []
    const a1 = []
    for (let i = 0; i < n; i++) {
      const v1 = g1.next().value
      const tk = Math.floor(v1 * k)
      a1.push({ x: i + 1, y: v1 })
      k1[tk] = k1[tk] ? k1[tk] + 1 : 1
    }
    this.setState({
      a1,
      k,
      k1: k1.map((v, i) => ({ x: i + 1, y: v }))
    })
  }

  render() {
    const {
      n,
      m,
      a1,
      k1,
      k,
    } = this.state
    return (
      <div>
        <p>
          m :
          <input
            value={m}
            onChange={e => this.setState({ m: e.target.value })}
          />
        </p>
        <p>
          n :
          <input
            value={n}
            onChange={e => this.setState({ n: e.target.value })}
          />
        </p>
        <p>
          <button onClick={this.update}>
            update
          </button>
        </p>
        <VictoryChart
          domainPadding={20}
          theme={VictoryTheme.material}
        >
          <VictoryLine
            data={a1}
            interpolation='basis'
            range={{ x: [0, n], y: [0, 1] }}
          />
        </VictoryChart>
        <VictoryChart
          domainPadding={20}
          theme={VictoryTheme.material}
        >
          <VictoryLine
            data={k1}
            interpolation='basis'
          />
          <VictoryLine
            data={[n / k]}
          />
        </VictoryChart>
      </div>
    );
  }
}

export default App;

