// @flow
import { getConnectionManager, Repository } from 'typeorm';
import {Organization} from '../models/Organization'

const db = (): Repository<Organization> => {
  return getConnectionManager().get().getRepository(Organization);
};

// Create a organization
const createOrganization = async (name: string): Promise<Organization> => {
  try {
    const org = new Organization();
    org.name = name;
    await db().persist(org);
    return org;
  } catch (e) {
    console.log(e);
    throw new Error('Problem creating organization!');
  }
};

// Get a organization by Id
const getOrgById = async (id: number): Promise<?Organization> => {
  try {
    const org = await db().findOneById(id);
    return org;
  } catch (e) {
    throw new Error(`Problem getting organization by id: ${id}!`);
  }
};

// Get organizations
const getOrganizations = async (): Promise<Array<Organization>> => {
  try {
    const org = await db().createQueryBuilder('organizations')
      .getMany();
    return org;
  } catch (e) {
    throw new Error('Problem getting organizations!');
  }
};

export default {
  createOrganization,
  getOrgById,
  getOrganizations
};
