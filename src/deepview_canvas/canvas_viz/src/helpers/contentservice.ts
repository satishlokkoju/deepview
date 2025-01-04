/**
 * Copyright 2024 BetterWithData
 * 
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * 
 *     http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License. 
 */


import { ContentsManager, Contents } from '@jupyterlab/services';

/**
 * Singleton contentsService class for managing file operations
 */
export class ContentsService {
  contentsManager: ContentsManager;
  private static instance: ContentsService;
  private baseServerPath: string;

  private constructor() {
    const contentsManager = new ContentsManager();
    this.contentsManager = contentsManager;
    // Get the server root from the contents manager settings
    this.baseServerPath = contentsManager.serverSettings?.baseUrl || process.env.JUPYTER_SERVER_ROOT || '';
  }

  static getInstance(): ContentsService {
    if (!this.instance) {
      this.instance = new ContentsService();
    }
    return this.instance;
  }

  /**
   * Create a file/directory if it does not exist. Otherwise, save the change in a file/directory in the given path
   * @param path path to a file/directory
   * @param options options that specify if it's a file or directory and additial information
   * Usage: save('snippets', { type: 'directory' }) to create/save a directory
   *        save('snippets/test.json', {type: 'file', format: 'text', content: 'Lorem ipsum dolor sit amet'})
   */
  async save(
    path: string,
    options?: Partial<Contents.IModel>
  ): Promise<Contents.IModel> {
    try {
      const changedModel = await this.contentsManager.save(path, options);
      return changedModel;
    } catch (error) {
        console.error('Error saving file/directory:', error);
        throw error; // Re-throw the error instead of returning it
    }
  }
  
  async readContent(
    path: string
  ): Promise<string> {
    try {
      const getFileResult = await this.contentsManager.get(path);
      if (typeof getFileResult.content !== 'string') {
        throw new Error('Unable to read the image');
      }
      return `data:${getFileResult.mimetype};${getFileResult.format},${getFileResult.content}`;
    } catch (error) {
        console.error('Error reading file/directory:', error);
        throw error; // Re-throw the error instead of returning it
    }
  }

  async readAudioContent(
    path: string
  ): Promise<string> {
    try {
      const getFileResult = await this.contentsManager.get(path);
      if (typeof getFileResult.content !== 'string') {
        throw new Error('Unable to read the Audio data');
      }
      return `${getFileResult.content}`;
    } catch (error) {
        console.error('Error reading file/directory:', error);
        throw error; // Re-throw the error instead of returning it
    }
  }

  /**
   * Convert a server path to a local filesystem path
   * @param path - Server path (e.g., '/notebooks/example.ipynb')
   * @returns Local filesystem path (e.g., '/home/user/notebooks/example.ipynb')
   * 
   * Usage:
   * ```typescript
   * const serverPath = '/notebooks/example.ipynb';
   * const localPath = contentsService.getLocalPath(serverPath);
   * console.log(localPath); // '/home/user/notebooks/example.ipynb'
   * ```
   */
  getLocalPath(path: string): string {
    const relativePath = this.contentsManager.localPath(path);
    if (!this.baseServerPath) {
      console.warn('Base server path not available, returning relative path');
      return relativePath;
    }
    return `${this.baseServerPath}/${relativePath}`.replace(/\/+/g, '/'); // Clean up any double slashes
  }

  /**
   * Convert a local filesystem path to a server path
   * @param localPath - Local filesystem path (e.g., '/home/user/notebooks/example.ipynb')
   * @returns Server path (e.g., '/notebooks/example.ipynb')
   * 
   * Usage:
   * ```typescript
   * const localPath = '/home/user/notebooks/example.ipynb';
   * const serverPath = contentsService.getServerPath(localPath);
   * console.log(serverPath); // '/notebooks/example.ipynb'
   * ```
   */
  getServerPath(localPath: string): string {
    return this.contentsManager.normalize(localPath);
  }

  /**
   * Resolve a relative path against a parent directory
   * @param relativePath - Relative path to resolve (e.g., '../data/file.csv')
   * @param parent - Parent directory to resolve against (e.g., '/notebooks/project')
   * @returns Resolved absolute server path
   * 
   * Usage:
   * ```typescript
   * // When in /notebooks/project/analysis
   * const relativePath = '../data/file.csv';
   * const parent = '/notebooks/project/analysis';
   * const resolved = contentsService.resolvePath(relativePath, parent);
   * console.log(resolved); // '/notebooks/project/data/file.csv'
   * 
   * // Handle special cases
   * contentsService.resolvePath('.', '/home');        // Returns '/home'
   * contentsService.resolvePath('..', '/home/user');  // Returns '/home'
   * contentsService.resolvePath('file.txt', '/dir');  // Returns '/dir/file.txt'
   * ```
   */
  resolvePath(relativePath: string, parent: string): string {
    return this.contentsManager.resolvePath(relativePath, parent);
  }
}
