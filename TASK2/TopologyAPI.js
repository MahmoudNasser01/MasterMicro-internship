const fs = require('fs');
const path = require('path');
const promisify = require('util').promisify;

const readFile = promisify(fs.readFile);
const writeFile = promisify(fs.writeFile);




/*
//   __________________
//  | ________________ |
//  ||                ||
//  ||[Program Agenda]||
//  ||                ||
//  ||                ||
//  ||________________||
//  |__________________|B
//  \###################\U
//   \###################\N
//    \        ____       \N
//     \_______\___\_______\Y


- Return all topologies in memory
- Read / Write from Json file 
- Delete topology from memory
- Return all devices of a topology with the given id and netlistNodeID


*/


/**
 * Topology API library class
 *@class ToplogyAPI
 */

class TopologyAPI {
    
    /**
     * TopologyAPI class constuctor
     * 
     */

    constructor() {
        /**
         * stor topologies in memory
         */
        this.topologies = []
    }


       /**
     * return all topologies in memory
     * 
     * (return) --> <Array of objects>
     * 
     */
        async queryTopologies() {
            return this.topologies;
        }

    /**
     * Get topology by ID
     * (params) --> id
     * (return) --> the topolgy object with that id
     */
    getTopology(id) {
        const result = this.topologies.filter(topology => topology.id === id);

        if (result.length == 0)
            return null;

        return result[0];
    }

 

    /**
     * Read Json 
     */
    async readJson(fileName) {
        const data = await readFile(path.resolve() + `/${fileName}.json`);
        const topology = JSON.parse(data);

        this.topologies.push(topology);

        return topology;
    }

    /**
     * Write Json
     */
    async writeJson(id) {
            const topology = this.getTopology(id);

            if (!topology) {
                return null;
            }

            await writeFile(path.resolve() + `/output/topology_${id}.json`, JSON.stringify(topology));

            return topology;
        }
        /**
         * Delete topology from memory
         */
    async deleteTopology(id) {
        const deletedTopology = this.getTopology(id);

        if (!deletedTopology) {
            return null;
        }

        this.topologies = this.topologies.filter(topology => topology.id !== id);
        return deletedTopology;
    }

    /**
     * return all devices of a topology with the given id
     */
    async queryDevices(id) {
        const topology = this.getTopology(id);

        if (!topology) {
            return null;
        }
        const { components } = topology;
        return components;
    }

    /**
     * return all devices of a topology with the given id and netlistNodeID
     */
    async queryDevicesWithNetlistNode(id, netlistNodeID) {
        const topology = this.getTopology(id);

        if (!topology) {
            return null;
        }

        const { components } = topology;

        const result = [];

        components.forEach(component => {

            for (const netlistNode of Object.values(component.netlist)) {
                if (netlistNode === netlistNodeID) {
                    result.push(component);
                    break;
                }
            }
        });

        return result;
    }
}


// Here we Test The components

async function test() {
    const obj = new TopologyAPI();

    await obj.readJson('topology');
    await obj.queryTopologies();
    await obj.deleteTopology("top1");
}

test();


module.exports = TopologyAPI;